# V380 Camera Monitoring Application

This project is a camera monitoring application that provides real-time video streaming and object detection using YOLOv8. It also supports PTZ (Pan-Tilt-Zoom) control for the camera.
## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AminNaghiyan/V380_object_detection.git
    cd V380_object_detection
    ```

2. Install the dependencies:
    - Install requirements.txt packages

    ```bash
    pip install -r requirements.txt
    ```
    - Install [Onvif](https://github.com/FalkTannhaeuser/python-onvif-zeep) package
    ```bash
    git clone https://github.com/FalkTannhaeuser/python-onvif-zeep.git
    cd python-onvif-zeep && python setup.py install
    or
    pip install --upgrade onvif_zeep
    ```
    - Install [CUDA](https://developer.nvidia.com/cuda-downloads)
    - Install [pytorch](https://pytorch.org/get-started/locally/)
## Configuration

1. Update the `utils/config.py` file with your camera's IP address, username, and password:

    ```python
    # utils/config.py

    CAMERA_CONFIG = {
        "usr": "admin",
        "pwd": "yourpassword",
        "ip": "yourcameraip"
    }
    ```

2. Change the `wsdl_path` parameter in `ptz_control.py` to point to the correct WSDL file location for your PTZ camera:

    ```python
    # ptz_control.py

    wsdl_path = "path_to_your_wsdl_file"
    ```
## Usage

  To run the application, simply execute the `main.py` file.
