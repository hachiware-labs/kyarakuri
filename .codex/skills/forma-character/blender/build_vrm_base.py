from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a base Blender scene for later VRM work.")
    parser.add_argument("--output-blend", type=Path, required=True)
    parser.add_argument("--review-render", type=Path, required=True)
    parser.add_argument("--result-json", type=Path, required=True)
    parser.add_argument("--texture-image", type=Path, default=None)
    return parser.parse_args(argv)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def first_mesh_object() -> bpy.types.Object:
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            return obj
    raise RuntimeError("No mesh object was found in the opened blend file.")


def ensure_camera(scene: bpy.types.Scene) -> bpy.types.Object:
    if scene.camera is not None:
        return scene.camera

    camera_data = bpy.data.cameras.new(name="KyarakuriCamera")
    camera_object = bpy.data.objects.new(name="KyarakuriCamera", object_data=camera_data)
    scene.collection.objects.link(camera_object)
    camera_object.location = (0.0, -3.2, 1.5)
    camera_object.rotation_euler = (1.3089969, 0.0, 0.0)
    scene.camera = camera_object
    return camera_object


def ensure_light(scene: bpy.types.Scene) -> bpy.types.Object:
    for obj in scene.objects:
        if obj.type == "LIGHT":
            return obj

    light_data = bpy.data.lights.new(name="KyarakuriSun", type="SUN")
    light_object = bpy.data.objects.new(name="KyarakuriSun", object_data=light_data)
    scene.collection.objects.link(light_object)
    light_object.location = (2.0, -2.0, 4.0)
    light_object.rotation_euler = (0.7853982, 0.0, 0.7853982)
    return light_object


def ensure_material(mesh_object: bpy.types.Object) -> bpy.types.Material:
    if mesh_object.data.materials:
        material = mesh_object.data.materials[0]
    else:
        material = bpy.data.materials.new(name="KyarakuriMaterial")
        mesh_object.data.materials.append(material)
    material.use_nodes = True
    return material


def ensure_principled_setup(material: bpy.types.Material) -> tuple[bpy.types.Node, bpy.types.NodeTree]:
    node_tree = material.node_tree
    nodes = node_tree.nodes
    links = node_tree.links

    principled = next((node for node in nodes if node.type == "BSDF_PRINCIPLED"), None)
    if principled is None:
        principled = nodes.new(type="ShaderNodeBsdfPrincipled")
        principled.location = (0.0, 0.0)

    output = next((node for node in nodes if node.type == "OUTPUT_MATERIAL"), None)
    if output is None:
        output = nodes.new(type="ShaderNodeOutputMaterial")
        output.location = (250.0, 0.0)

    if not any(link.from_node == principled and link.to_node == output for link in links):
        links.new(principled.outputs["BSDF"], output.inputs["Surface"])

    return principled, node_tree


def apply_texture(material: bpy.types.Material, texture_image: Path) -> str:
    if not texture_image.exists():
        raise RuntimeError(f"Texture image was not found: {texture_image}")

    principled, node_tree = ensure_principled_setup(material)
    nodes = node_tree.nodes
    links = node_tree.links

    tex_node = next((node for node in nodes if node.type == "TEX_IMAGE"), None)
    if tex_node is None:
        tex_node = nodes.new(type="ShaderNodeTexImage")
        tex_node.location = (-250.0, 0.0)

    tex_node.image = bpy.data.images.load(filepath=str(texture_image), check_existing=True)
    for link in list(links):
        if link.to_node == principled and link.to_socket == principled.inputs["Base Color"]:
            links.remove(link)
    links.new(tex_node.outputs["Color"], principled.inputs["Base Color"])
    return tex_node.image.filepath


def configure_render(scene: bpy.types.Scene, review_render: Path) -> None:
    ensure_parent(review_render)
    scene.render.filepath = str(review_render)
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100


def save_result_json(path: Path, payload: dict[str, object]) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def run(argv: list[str]) -> int:
    args = parse_args(argv)
    scene = bpy.context.scene
    mesh_object = first_mesh_object()
    material = ensure_material(mesh_object)
    texture_applied = None
    if args.texture_image is not None:
        texture_applied = apply_texture(material, args.texture_image)
    else:
        ensure_principled_setup(material)

    camera = ensure_camera(scene)
    light = ensure_light(scene)
    configure_render(scene, args.review_render)

    ensure_parent(args.output_blend)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output_blend))
    bpy.ops.render.render(write_still=True)

    save_result_json(
        args.result_json,
        {
            "mesh_object": mesh_object.name,
            "material": material.name,
            "texture_applied": texture_applied,
            "camera": camera.name,
            "light": light.name,
            "output_blend": str(args.output_blend),
            "review_render": str(args.review_render),
        },
    )
    return 0


def main() -> int:
    argv = sys.argv
    forwarded = argv[argv.index("--") + 1 :] if "--" in argv else []
    try:
        return run(forwarded)
    except Exception as exc:  # noqa: BLE001
        print(f"build_vrm_base.py failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
