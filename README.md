# DAC 2026 - AI Hardware Attack Challenge
 [![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

[![](https://dcbadge.limes.pink/api/server/https://discord.gg/mVhGtUmu8)](https://discord.gg/mVhGtUmu8)

Welcome to the IEEE DAC 2026 AI Hardware Attack (AHA!) Challenge, offered as part of the [GREAT (Gen-AI Red-Team Evaluation of Microelectronics Assurance and Trust) workshop](https://63dac.conference-program.com/presentation/?id=WKSHP104&sess=sess198)!

In this competition teams are challenged to use generative AI to both insert hardware Trojans into FPGA-targeted hardware designs as well as determine their exploits for these new Trojans. The competition is broken into two phases: a fully-virtual simulation-based phase, and a hybrid virtual/in-person phase for the finalists. The target of this competition is the [Hackster](https://calico.computer/) board from Calico Computer, an education-focused device which includes an application microprocessor, an FPGA, and additional peripherals aimed at hardware security education. Finalists will receive Hackster boards at DAC as part of the in-person competition.

*Note: Please be aware, as the second phase is hybrid remote and in-person at DAC, teams selected as finalists are expected to have at least one member attending DAC to compete in the in-person challenge.*

**Register Here:** https://forms.gle/6fJ8ZmrSu6B4BnU99

## Table of Contents
- [Table of Contents](#table-of-contents)
- [General Guidelines](#general-guidelines)
  - [Timeline](#timeline)
  - [Teams](#teams)
  - [Communication](#communication)
  - [AI Usage](#ai-usage)
- [Phase 1](#phase-1)
  - [Setup](#setup)
  - [Challenge](#challenge)
  - [Phase 1 Deliverables](#phase-1-deliverables)
  - [Scoring](#scoring)
- [Phase 2](#phase-2)
- [Getting Started](#getting-started)
- [Hackster Board](#hackster-board)
- [Previous Competitions](#previous-competitions)

## General Guidelines
### Timeline
- 23 May: Challenge Phase 1 Launch
- 13 June: Phase 1 Submission Deadline
- 17 June: Finalists Notified
- 22 June: Phase 2 Launch
- 26 July: GREAT Workshop @ DAC

*Note: There is no registration deadline. Teams can register and submit up until the Phase 1 submission deadline.*
### Teams
This competition accepts teams from any affiliation (industry, academia, etc.). Teams can consist of up to 4 members, with academically-affiliated teams expected to also include an advisor.

### Communication
The majority of communications about this and future competitions will be done through our Discord server. [Please feel free to join.](https://discord.gg/mVhGtUmu8)

### AI Usage
This competition relies on significant use of generative AI. As such, detailed logs need to be kept and included in all submissions, detailing every interaction with AI. **If a submission is made without logs or the logs are missing key information, the submission may be disqualified.**

## Phase 1
The [Phase 1 challenge description](./phase_1/README.md) can be found in the [Phase 1 directory](./phase_1/).

## Phase 2
Phase 2 consists of three separate challenges, two of which are released as of 1 July and detailed in the [Phase 2 directory](./phase_2/).

Phase 2 will conclude with a final challenge at the [GREAT Workshop](https://63dac.conference-program.com/presentation/?id=WKSHP104&sess=sess198) at DAC 2026. During this workshop, teams will be asked to demonstrate their Trojans on [Hackster boards](https://calico.computer/) and will be given a *final challenge to be completed during the duration of the workshop*.

## Getting Started
We recommend the [Yosys OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build) for use with the Hackster board. It contains all of the tools that teams should need to get started such as:
- Icarus Verilog
- GTKWave
- Yosys
- IceStorm

While you are not required to use these specific tools, the Hackster was designed to work with open-source tooling such as this.

For the first phase of the competition, teams will not have access to a physical Hackster board, however, [this documentation](https://cgi.cse.unsw.edu.au/~cs6420/labs/lab00introduction/) on getting the Hackster set up (with the OSS CAD Suite) could prove helpful in understanding the connections on the board and how the whole system is built. You can also see the [hackster-programmer GitHub](https://github.com/kiwih/hackster-programmer) repo for additional information like the PCB schematics.

## Hackster Board
The *Hackster* board from Calico Computer is a hardware security learning platform designed by Dr. Hammond Pearce. It contains an application processor ([RP2040](https://www.raspberrypi.com/products/rp2040/)), a programming processor (RP2040), FPGA ([iCE40-UP5K](https://www.latticesemi.com/en/products/fpgaandcpld/ice40ultraplus)), and additional circuitry and components for side-channel power analysis.

The Hackster hardware is under the CC BY-SA 4.0 license. Any use of the hardware documentation (such as the schematic) or the gerber files for the Hackster should be attributed as follows:

"Hammond Pearce, UNSW Sydney - CC BY-SA 4.0"

## Previous Competitions
We've run versions of this competition for the past several years at [NYU's CSAW Event](https://www.csaw.io/ai-hardware-attack-challenge). We also [published results from the first two competitions](https://ieeexplore.ieee.org/document/11169309), which might help serve as inspiration if you find your team is stuck.

