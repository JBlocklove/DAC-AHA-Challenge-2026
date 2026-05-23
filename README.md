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
One major use for FPGAs is to accelerate often computationally expensive and slow cryptographic processes. In this phase, your target is a simplified cryptographic accelerator implemented on the FPGA (a [Lattice iCE40-UP5K](https://www.latticesemi.com/en/products/fpgaandcpld/ice40ultraplus)), which communicates with the application microprocessor ([RP2040](https://www.raspberrypi.com/products/rp2040/)) on the Hackster over a SPI (Serial Peripheral Interface) bus. However, the source RTL will not be provided for this design; instead, teams must reverse engineer the provided bitstream to determine how the cryptographic algorithm works before they can then add hardware Trojans. While existing non-AI tools may be leveraged throughout the challenge, the hardware Trojan and exploit must be written fully with AI.


### The Setup
The RP2040 acts as the SPI controller, sending plaintext data and cryptographic keys to the FPGA (the SPI peripheral). The FPGA processes this data through its hardware accelerator and transmits the resulting ciphertext back to the RP2040. 

For Phase 1, teams will be operating entirely in simulation. The following can be found in the [Phase 1 directory](./phase_1) in this repo:
- **FPGA Bitstream:** The bitstream for the Lattice [iCE40 UltraPlus FPGA](https://www.latticesemi.com/en/products/fpgaandcpld/ice40ultraplus).
- **Micropython Application Code:** The micropython software for the [RP2040](https://www.raspberrypi.com/products/rp2040/) which interacts with the FPGA IP core. This should be used to create a testbench once a functional Verilog module has been recovered from the bitstream.
- **FPGA Interface Documentation:** Simple documentation explaining how the interaction with the FPGA works, including details on SPI speeds, expected timing, and signals between the RP2040 and FPGA.

Please see the [*Getting Started section*](#getting-started) for details on the open-source tooling we recommend and a general guide on using the Hackster. *Note: You are not required to only use these open-source tools, they are only provided as a starting point.*

### The Challenge
Your objective is to use generative AI to design and insert a stealthy *hardware Trojan* into the recovered RTL from the provided bitstream. The Trojan must be designed such that the accelerator functions perfectly under normal conditions, but malicious behavior is activated under specific, hidden circumstances.

**No hardware may be written by human users. This will be confirmed with the submitted AI logs.**

To successfully complete this phase, your GenAI-assisted Trojan must feature:
- **A Trigger:** A specific sequence of events or data that activates the Trojan.
- **A Payload:** The malicious action taken once triggered. For example, leaking the secret cryptographic key over the SPI MISO line, silently weakening the encryption, or predictably corrupting the ciphertext.

Your modified design does not need to remain in the exact format that the bitstream was recovered into, the AI is able to rename variables and create additional modules as it sees fit.

### Phase 1 Deliverables
By the submission deadline, teams must provide a `.zip` archive containing:

1.  **Modified RTL:** The Verilog files containing your AI-generated hardware Trojan.
2.  **Exploit Testbench:** A custom simulation testbench demonstrating how to trigger the Trojan and verifying that the payload successfully executes.
    - This can be based off the provided funtional micropython script.
3.  **GenAI Transcripts:** Comprehensive logs (or a document containing links to chat histories) of all prompts and AI responses used to generate the Trojan. *Submissions missing these logs will be disqualified.*
4.  **Technical Brief:** A short text or markdown README detailing the following:
    - The team's methods for reverse engineering and understanding the bitstream.
    - The team's methods for using AI to analyze the design and generate the Trojan. This should include details on the method of interaction (API, website UI, etc.), the model(s) used, and any additional supporting framework that might have been used around the AI. *This is largely what we will be judging to determine points for creative AI usage.*
    - Details about the Trojan's design, including:
        - Information about the trigger and payload.
        - Any methods taken to increase the Trojan's stealth.
        - Details on the exploit for the vulnerability. **This should include enough detail that we are able to exploit the Trojan in hardware once a bitstream is generated from the provided RTL.**

All files should be submitted in the following format to [this Google form](https://forms.gle/kRLwy3NoLW7wVj4w8):
```
submission.zip
├── README.md (or pdf)
├─ rtl/
│  └── <Modified RTL>
├─ tb/
│  └── <Exploit Testbench>
└─ ai/
   └── <all AI interactions (chat logs, etc.)>
```

### Scoring
The following rubric depicts how the first phase of the challenge will be judged:

#### Creative Use of Generative AI
Evaluates the sophistication of the AI pipeline (e.g., complex prompt chaining and engineering, RAG, agentic workflows, etc.) versus basic copy-pasting.

| | Exemplary  <br> 35 - 28 Points| Proficient <br> 27 - 18 Points | Developing <br> 17 - 9 Points | Novice <br> 8 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Generative AI Use** | Dynamic, seamless AI generation and insertion using advanced techniques (e.g., AST manipulation). | Effective AI generation of logic, but relies on little more than prompt engineering and basic insertion. | Simple AI generated logic, but required significant manual editing through repeated prompting. | Minimal AI use; just simple prompting with copy-pasting. |

#### Trojan Quality
Evaluates the quality of the generated Trojan for factors like stealth, severity, and funtionality in-situ

| | Exemplary  <br> 25 - 20 Points| Proficient <br> 19 - 13 Points | Developing <br> 12 - 6 Points | Novice <br> 5 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Trojan Quality** | Highly stealthy with an extremely specific trigger and negligible resource overhead. Payload is sophisticated (e.g., precise key exfiltration) and normal operation is perfectly preserved. | Stealthy with a clear trigger and functional payload. Normal operation is preserved, but resource overhead is noticeable or the payload is less sophisticated (e.g., simple DoS or basic data corruption). | Trojan activates, but the trigger is too broad (prone to accidental activation). Normal operation is occasionally impacted, or the hardware footprint is suspiciously large. | Trojan fails to trigger, completely breaks the baseline cryptographic functionality, or the payload is non-functional. |


#### System Automation
Measures the end-to-end automation of the generation, insertion, and testing pipeline.

| | Exemplary  <br> 15 - 12 Points| Proficient <br> 11 - 8 Points | Developing <br> 7 - 4 Points | Novice <br> 3 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **System Automation** | Fully automated, "one-click" pipeline from AI generation to simulation output. |  Highly automated but requires 1-2 manual steps (e.g., moving files). |Fragmented pipeline requiring manual oversight and handoffs between scripts.  |No automation; entirely manual generation, insertion, and testing.  |

#### Documentation & Reproducibility
Evaluates the clarity of the team's write-up, full AI logs, and instructions for replicating the exploit/using the generative AI framework.

| | Exemplary  <br> 15 - 12 Points| Proficient <br> 11 - 8 Points | Developing <br> 7 - 4 Points | Novice <br> 3 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Documentation** | Exceptional detail on AI prompts, architecture, and perfect reproducibility steps. | Clear and complete explanation of strategy and mechanism; mostly reproducible. | Basic overview lacking pipeline details; reproducibility requires guesswork. | Missing or highly confusing; fails to explain AI usage or Trojan operation. |


#### Exploitation Simulation
Assesses the quality of the testbench in proving both normal operation and the successful Trojan exploit.

| | Exemplary  <br> 10 - 8 Points| Proficient <br> 7 - 5 Points | Developing <br> 4 - 2 Points | Novice <br> 1 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Simulation Quality** | Flawless testbench; explicitly proves normal operation *and* the payload trigger with clear waveforms. | Clearly demonstrates payload triggering, but proof of normal operation is lacking. | Buggy or hard to interpret; proves payload works but trigger mechanism is unclear. | Missing, fails to compile, or does not successfully demonstrate the exploit. |

#### Bonus Points
While not explicitly a part of this particular challenge, up to 10 bonus points are available if teams can recover the key used for encryption/decryption in the FPGA accelerator. **If you do so, please make it clear in your documentation along with a brief explanation of how you recovered the key.**

## Phase 2
**To be released at the start of Phase 2.**

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

