from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply an imported BVH motion and render one preview frame.")
    parser.add_argument("--motion-file", type=Path, required=True)
    parser.add_argument("--output-blend", type=Path, required=True)
    parser.add_argument("--preview-render", type=Path, required=True)
    parser.add_argument("--result-json", type=Path, required=True)
    return parser.parse_args(argv)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def first_existing_armature() -> bpy.types.Object:
    for obj in bpy.context.scene.objects:
        if obj.type == "ARMATURE":
            return obj
    raise RuntimeError("No armature object was found in the opened blend file.")


def ensure_camera(scene: bpy.types.Scene) -> bpy.types.Object:
    if scene.camera is not None:
        return scene.camera

    camera_data = bpy.data.cameras.new(name="KyarakuriMotionCamera")
    camera_object = bpy.data.objects.new(name="KyarakuriMotionCamera", object_data=camera_data)
    scene.collection.objects.link(camera_object)
    camera_object.location = (0.0, -3.5, 1.6)
    camera_object.rotation_euler = (1.3089969, 0.0, 0.0)
    scene.camera = camera_object
    return camera_object


def ensure_light(scene: bpy.types.Scene) -> bpy.types.Object:
    for obj in scene.objects:
        if obj.type == "LIGHT":
            return obj

    light_data = bpy.data.lights.new(name="KyarakuriMotionSun", type="SUN")
    light_object = bpy.data.objects.new(name="KyarakuriMotionSun", object_data=light_data)
    scene.collection.objects.link(light_object)
    light_object.location = (2.0, -2.0, 4.0)
    light_object.rotation_euler = (0.7853982, 0.0, 0.7853982)
    return light_object


def import_bvh(motion_file: Path) -> bpy.types.Object:
    if not motion_file.exists():
        raise RuntimeError(f"BVH motion file was not found: {motion_file}")

    before_names = {obj.name for obj in bpy.context.scene.objects}
    bpy.ops.import_anim.bvh(filepath=str(motion_file))
    new_armatures = [
        obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE" and obj.name not in before_names
    ]
    if new_armatures:
        return new_armatures[0]

    active_object = bpy.context.active_object
    if active_object is not None and active_object.type == "ARMATURE":
        return active_object

    raise RuntimeError("BVH import completed but no imported armature was found.")


def assign_motion(target_armature: bpy.types.Object, source_armature: bpy.types.Object) -> tuple[str, int]:
    if source_armature.animation_data is None or source_armature.animation_data.action is None:
        raise RuntimeError("Imported BVH armature does not contain an animation action.")

    source_action = source_armature.animation_data.action
    target_armature.animation_data_create()
    copied_action = source_action.copy()
    target_armature.animation_data.action = copied_action
    frame_start = int(copied_action.frame_range[0])
    frame_end = int(copied_action.frame_range[1])
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end
    return copied_action.name, frame_start


def remove_imported_armature(imported_armature: bpy.types.Object, target_armature: bpy.types.Object) -> None:
    if imported_armature == target_armature:
        return
    armature_data = imported_armature.data
    bpy.data.objects.remove(imported_armature, do_unlink=True)
    if armature_data is not None and armature_data.users == 0:
        bpy.data.armatures.remove(armature_data)


def configure_render(scene: bpy.types.Scene, preview_render: Path) -> None:
    ensure_parent(preview_render)
    scene.render.filepath = str(preview_render)
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
    target_armature = first_existing_armature()
    imported_armature = import_bvh(args.motion_file)
    action_name, preview_frame = assign_motion(target_armature, imported_armature)
    remove_imported_armature(imported_armature, target_armature)

    camera = ensure_camera(scene)
    light = ensure_light(scene)
    configure_render(scene, args.preview_render)
    scene.frame_set(preview_frame)

    ensure_parent(args.output_blend)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output_blend))
    bpy.ops.render.render(write_still=True)

    save_result_json(
        args.result_json,
        {
            "target_armature": target_armature.name,
            "action_name": action_name,
            "preview_frame": preview_frame,
            "camera": camera.name,
            "light": light.name,
            "motion_file": str(args.motion_file),
            "output_blend": str(args.output_blend),
            "preview_render": str(args.preview_render),
        },
    )
    return 0


def main() -> int:
    argv = sys.argv
    forwarded = argv[argv.index("--") + 1 :] if "--" in argv else []
    try:
        return run(forwarded)
    except Exception as exc:  # noqa: BLE001
        print(f"apply_motion_preview.py failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
