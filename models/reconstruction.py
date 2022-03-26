from models.camera import Camera, json_parse_camera
from models.point import Point, json_parse_point
from models.shot import Shot, json_parse_shot


class Reconstruction:
    cameras: dict[str, Camera] = {}
    shots: list[Shot] = []
    points: list[Point] = []

    def add_camera(self, name: str, camera: Camera):
        self.cameras[name] = camera

    def add_shot(self, shot: Shot):
        self.shots.append(shot)

    def add_point(self, point: Point):
        self.points.append(point)


class ReconstructionCollection:
    reconstructions: list[Reconstruction] = []

    def append(self, reconstruction: Reconstruction):
        self.reconstructions.append(reconstruction)

    def __getitem__(self, i: int):
        return self.reconstructions[i]

    def __len__(self):
        return len(self.reconstructions)


def json_parse_reconstruction(el: dict) -> Reconstruction:
    reconstruction = Reconstruction()
    for name, ela in el['cameras'].items():
        reconstruction.add_camera(name, json_parse_camera(ela))

    for image_name, ela in el['shots'].items():
        reconstruction.add_shot(json_parse_shot(image_name, ela, reconstruction.cameras))

    for name, ela in el['points'].items():
        reconstruction.add_point(json_parse_point(name, ela))

    return reconstruction


def json_parse_reconstruction_collection(el: dict) -> ReconstructionCollection:
    rc = ReconstructionCollection()
    for elr in el:
        rc.append(json_parse_reconstruction(elr))
    return rc