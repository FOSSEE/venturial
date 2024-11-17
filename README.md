Venturial: A GUI for OpenFOAM
-----------------------------------------------------

Venturial is a Blender addon that alleviates the effort to build OpenFOAM cases.

Venturial seeks to procedurally introduce OpenFOAM’s case-building process to newcomers through instructive interfaces that are optionally customizable for the succinct needs of experienced users and graphically modifiable for domain-specific work. It provides an expedient workflow via interactive tools that facilitate OpenFOAM's case-definition rules without diminishing user control.  

The main features are:

1. Compose hexahedral primitives within Blender to generate blockmesh dictionary. 
2. Import CAD files into Blender and generate snappyhexmesh dictionary with Venturial's geometry setup tools.
3. Import mesh dictionaries and convert geometry definitions to Blender-editable objects for modification and re-composition.
4. Visualize mesh structural data with hovering annotations. 
5. Graphically customize solver parameters for domain-specific solution modeling.    
6. Use editable case file templates to populate an OpenFOAM case.  
7. Control and monitor solver execution.

Venturial also comes with convenience tools such as a case-file manager, auto-saving, keyboard shortcuts and an in-built tutorial and documentation tool. 

Genesis
-----------------------------------------------------

Venturial is inspired from [reynolds-blender](https://github.com/dmsurti/reynolds-blender), a reference implementation of [reynolds](https://github.com/dmsurti/reynolds). It is among the open-sourced software products built by the [FOSSEE](https://fossee.in/) project at [IIT Bombay](https://www.iitb.ac.in/) and managed by [CFD-FOSSEE Team](https://cfd.fossee.in/home). Venturial is presently under development and we hope to create a stable release soon. If you wish to contribute to Venturial or be a part of the development team, then reach out to us at contact-cfd@fossee.in. 

Installation
-----------------------------------------------------

Venturial is being developed as a cross-platform software. However, for the time being, we recommend using <em>Ubuntu 18.04LTS or 20.04 LTS</em>. Venturial is regularly updated, hence you should visit this repository for the latest features and upcoming release. As [WSL](https://ubuntu.com/wsl) is also a choice of platform for openfoam users, you can install Blender on windows, however some of Venturial's features may not work until a solution or a work around is found for them. 

Venturial installs like most other Blender-addons. Read more on [Blender addons](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html).

1. Visit Blender's [Download page](https://www.blender.org/download/) to find all versions of Blender. While we strive to keep our addon compatible with most versions of Blender, some Blender versions may include API patches that can cause errors with the Addon, hence for the time being we recommend to use Blender 3.2.1.
2. If you are using WSL, then download Blender for Windows from Blender's [Download page](https://www.blender.org/download/).
3. Within Blender, at the top bar, go to Edit >> Preferences. The Blender preferences window will open. Click the Addons section from the vertical menu. Click the install button. A file browser should open. Locate venturial's zip folder and click on the Install Add-on button.
4. Finally, enable venturial by clicking the checkbox. You are ready to use Venturial. 

Licensing
-----------------------------------------------------
1. Venturial is a free and fully open-sourced software built by the FOSSEE project and licensed under GPL 3.0.
2. Venturial is not approved or endorsed by OpenLimited, producer and distributor of the OpenFOAM software via www.openfoam.com, and owner of the OPENFOAM® and OpenCFD® trademarks.
3. Copyright (c) 2023 FOSSEE, CFD-FOSSEE.

Citations
-----------------------------------------------------
Venturial is a ongoing project and has several papers associated with it. We publish about recent developments to document essential progress milestones. 

A poster about Venturial was published in the [Proceedings of the 23rd Python in Science Conference](https://doi.org/10.25080/tpwg2365)
A short paper about Venturial's development process and history has been published in the [2023 IEEE T4E conference](https://doi.org/10.5281/zenodo.14162151)
Venturial was first published in the [18th OpenFOAM Workshop (OFW) 2023](https://oxford-abstracts.s3.amazonaws.com/83ca7ab4-c356-4411-be07-070eaeffd43a.pdf)
