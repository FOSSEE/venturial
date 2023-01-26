# Venturial: A GUI for OpenFOAM

Venturial, a Blender addon is a GUI application that alleviates the effort to construct OpenFOAM cases.

1. It provides a homogenous user interface to create geometries and graphically manipulate OpenFOAM dictionary templates.
2. It uses Blender as a development platform and the blender-python (bpy) API as the primary dependency of Venturial-tools.
3. It has an in-built tutorial and documentation tool to quickly learn its usage.

Venturial seeks to promote heuristic learning of OpenFOAM for newcomers and consists convenient tools to boost the productivity of OpenFOAM users. It provides an expedient workflow to generate OpenFOAM cases through Venturial-tools that automate OpenFOAM's case definition process without diminishing user control. The basic Venturial-tools systematically introduce fundamentals of OpemFOAM with minimal prerequisites. It is suggested that newcomers visit Venturial's usage tutorials. 

Venturial is inspired from [reynolds-blender](https://github.com/dmsurti/reynolds-blender), a reference implementation of [reynolds](https://github.com/dmsurti/reynolds). It is among the open-sourced software products built by the [FOSSEE](https://fossee.in/) project at [IIT Bombay](https://www.iitb.ac.in/) and managed by [CFD-FOSSEE Team](https://cfd.fossee.in/home). Venturial is presently under development and we hope to create a stable release soon. If you wish to contribute to Venturial or be a part of the development team, then reach out to us at contact-cfd@fossee.in. 

## Features:
Venturial-tools are built for specific purposes in steps following the process of solving a fluid-flow problem with OpenFOAM. Creating a successful OpenFOAM case requires these tools to work in tandem. Hence it is essential to know their features.

### 1. Meshing Features:
- Compose cell shapes (hexahedron, wedge, prism, pyramid, tetrahedron, tetrahedral wedge) graphically to construct editable-geometries.
- Query blockmesh-related data from geometries and export a blockmesh dictionary.
- Visualize geometry with hovering mesh parameters.

### 2. Case Definition Features:
- <em>Coming Soon</em>

### 3. Post-Processing Features:
- <em>Coming Soon</em>

### 4. Convenience Features:
- Changeable keyboard shortcuts for Venturial-tools.
- Customizable user-interface.
- Retain data with autosave.
- View tool usage with descriptive dialog boxes. 
- Run frequently used OpenFOAM commands through GUI widgets. 
- Open Paraview from Blender.

### 5. Upcoming Learning Features:
- View Venturial's usage tutorials on sample cases side-by-side with the Blender window. Keep track of your pace with a progress bar.
- View documentation of OpenFOAM solvers and their parameters.
- In-built quickstart guide.
- Contribute to Venturial-tutorials by submitting OpenFOAM case studies. 
- Report bugs to the Venturial development team. 
- Request a feature.

### 6. Other features in development
- Recompose geometry as a Blender-editable object by importing data from a non-programmable blockmesh dictionary.
- Use advanced blockmesh features for mergepatchpairs, geometries with curved edges, bafflesdict (in dev), symmetrical planes etc., to design more complex geometries.
- Set up a case with the available selection of solvers.
- Create/manipulate case data.
- Confirm the validity of case data before running a solver.
- Automatically interlink mesh data to relevant solver attributes.
- View Venturial's usage tutorials on sample cases side-by-side with the Blender window. Keep track of your pace with a progress bar.
- View documentation of OpenFOAM solvers and their parameters.
- In-built quickstart guide.
- Contribute to Venturial-tutorials by submitting OpenFOAM case studies. 
- Report bugs to the Venturial development team. 
- Request a feature.

## Installation:

Venturial is being developed as a cross-platform software. However, for the time being, we recommend using <em>Ubuntu 18.04LTS or 20.04 LTS</em>. Venturial is regularly updated, hence you should visit this repository for the latest features. Venturial is written in python with minimal dependencies so it currently doesn't require installation of external python packages. Future updates may involve such installation. As [WSL](https://ubuntu.com/wsl) is also a choice of platform for openfoam users, you can install venturial on windows, however some of its features may not work until a solution or a work around is found for them. 

### Steps
Venturial installs like most other Blender-addons. Read more on [Blender addons](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html).

1. Visit Blender's [Download page](https://www.blender.org/download/) to find all versions of Blender. While we strive to keep our addon compatible with most versions of Blender, some Blender versions may include API patches that can cause errors with the Addon, hence for the time being we recommend to use [Blender 3.2.1 linux](https://download.blender.org/release/Blender3.2/blender-3.2.1-linux-x64.tar.xz). Clicking the link should begin the download. The process for a ubuntu system on a virtual machine remains the same. 

2. If you are using WSL, then download Blender for Windows from Blender's [Download page](https://www.blender.org/download/) or click [here](https://download.blender.org/release/Blender3.2/blender-3.2.1-windows-x64.msi) to directly download Blender 3.2.1 on your windows system. Run the ```.msi``` file to install blender and jump to step 5.

3. Extract the compressed ```blender-3.2.1-linux-x64.tar.xz``` folder.
4. Enter the extracted folder and open a terminal there. Type ```./blender``` in the terminal. This will open Blender through the terminal.
5. Download venturial's zip folder from its github repository or by clicking on his link >> [Download Zip](https://github.com/FOSSEE/venturial/blob/main/venturial.zip). 
6. Make sure that the main folder inside the zip file is named ```venturial```. This allows ease of handling the addon.
7. Within Blender, at the top bar, go to Edit >> Preferences. The Blender preferences window will open. Click the Addons section from the vertical menu.
8. Click the install button. A file browser should open. Locate venturial's zip folder and click on the Install Add-on button.
9. Finally, enable venturial by clicking the checkbox. You are ready to use Venturial. 
10. Close Blender preferences window and return to the main window. While in Blender 3D Viewport ([What is 3D Viewport?](https://docs.blender.org/manual/en/latest/editors/3dview/index.html))  press the ```n``` button on your keyboard to unhide the [side-panel](https://docs.blender.org/manual/en/latest/editors/3dview/sidebar.html). Click on the tab named Venturial and expand the panel to your desired size.  
11. If you face issues with any of the above steps during installation then please let us know at contact-cfd@fossee.in. We would also like to hear issues due to different OS installations or virtual machines. As venturial develops, these issues are to likely subside.

### Best Practises:
- Visit Venturial's github page regularly to obtain the latest updates. This may be a manual process for now but we plan to incorporate an auto-update feature. 
- You will be playing around with Blender objects a lot. Know what [Blender objects](https://docs.blender.org/manual/en/latest/scene_layout/object/introduction.html) are. 
- Enable Venturial. Go to Edit >> Preferences and click the "Save & load" button at the bottom left corner of the window. In the menu click "Save Preferences" to avoid re-enabling.
- Go to Edit >> Preferences >> Keymap. In the Preferences section set <em>Select with Mouse Button</em> to "Right". In the 3D View section <em>select Middle Mouse Action</em> as "Orbit".
- It is worth knowing common [Blender shortcuts](https://docs.blender.org/manual/en/latest/interface/keymap/introduction.html).


### FAQ:

Q. What is Blender and why use it?

A. [Blender](https://www.blender.org/about/) is an open-sourced GUI based 3D computer graphics software. It provides a python API to manipulate geometric primitives and an integrated toolkit to draw user interface widgets. A collection of such widgets is called a Blender [Addon](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html).  

Q. Do I need to learn Blender to use Venturial?

A. No. Once Venturial is installed, you only need to learn Venturial's usage. It is designed to minimize dependency on Blender. However it is recommended to familiarize yourself with Blender. It is good to know the [basics](https://www.blender.org/support/).

Q. How do I update the new version of Venturial?

A. Updates are important. We will be rolling out new patches and features soon. To install a new version re-do steps 5 - 10. The zip file will be kept updated until beta release or an optional auto-update feature. Keep a single copy of the addon. If you install a new version, then remove the older version from Blender's config. To do this go to Edit >> Preferences >> Addons. In the search bar type ```Venturial```. Press the "Remove" button.

Q. I found a bug or a feature of Venturial is not working. What do I do?

A. Venturial is currently in development so we welcome your issues. You can either create an issue on github or contact us at contact-cfd@fossee.in. We will also incorporate a bug tracker and an integrated feature request tool soon. Once available it can be directly used to report issues.

## Compliance:
TBD

## Usage Policy:
TBD

## Licensing:
1. Venturial is a free and fully open-sourced software built by the FOSSEE project and licensed under GPL 3.0.
2. Venturial is not approved or endorsed by OpenLimited, producer and distributor of the OpenFOAM software via www.openfoam.com, and owner of the OPENFOAM® and OpenCFD® trademarks.
3. Copyright (c) 2023 FOSSEE, CFD-FOSSEE.
