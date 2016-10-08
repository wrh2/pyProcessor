# Project Report

This folder contains the project report.
It is availabe in markdown and pdf format.
To make changes to the report, you can edit
the markdown file and then use make to
create a new pdf. Note: this requires pandoc.

## Compile the report

    make

## Clean up pdf

    make clean

## Dependencies

* [Pandoc](http://pandoc.org/)

## Important notes about the report

This report describes the architecture for pyProcessor which is why I am making it available.
There are lots of details in here that are not necessary to understand the architecture.
At some point I will redo this documentation to reflect only the details that are important.
The report also makes mention of a non-hardware simulation version of pyProcessor.
This code has not been released and I don't plan to release it because it is not clock-accurate whereas the hardware simulation version is.
Lastly, this was a project for college so its not perfect.