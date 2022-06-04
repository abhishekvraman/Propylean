# Propylean
#### The open-source analytics package for chemical process industries

## What is Propylean
Propylean name is derived from words Process/Production + Python + lean programming/manufacturing.
Propylean is a Python library which will help engineers simulate production plants focusing on chemical and related process industries using only Python environments. 
By coupling this library with available data analysis/machine learning frameworks, engineers will be able to enhace operations of their plants. Ultimate aspiration of this project is to enable process industries transit to zero carbon operation.

## Objective
To increase the utilization of open-source software and analytics tools in the chemical and related industries.

## Vision
Vision of Propylean is to:
- Enable chemical and related industries to use analytics and ML frameworks
- Improve operational agility and efficiency of the plant
- Be a cheap simulation-software alternative for small manufacturers
- Help the industry transition to Net-Zero emissions
- Inculcate coding/programing skills in manufacturing engineers

## Installation and Requirements
To download use below command or download the wheel file from PyPi page.

Pip command:
`pip install propylean`

PyPi page:
https://pypi.org/project/propylean/

## Getting Started and Documentation
To get started with Propylean, have a look at the getting started documenation.
https://github.com/abhishekvraman/Propylean/wiki/Getting-started-with-Propylean

## Supported objects that can be imported:

* equipments.rotary
    1. CentrifugalPump
    2. PositiveDisplacementPump
    3. CentrifugalCompressor
* equipments.static
    1. PipeSegment
* equipments.exchangers
    1. AirCooler
    2. ElectricHeater
* instruments
    1. ControlValve
    2. FlowMeter
* streams
    1. MaterialStream
    2. EnergyStream
* properties
    1. Pressure
    2. Temperature
    3. MassFlowRate
    4. Components (Molecular components)
    5. And many more..