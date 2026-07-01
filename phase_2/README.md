# Phase 2 Challenges
The challenges in Phase 2 build upon the foundation established with the Phase 1 challenge, focusing again on the supply chain threat of inserting a hardware Trojan into an FPGA bitstream using documented IP cores. These challenges will be of similar design, but each contain a twist (an extra step, a specific kind of modification, etc.).


## The Setup
The setup for these challenges will again be similar to the challenge in Phase 1, leveraging the Hackster board as the target device for the attack. As such, the environment setup can once again be largely based on the [Getting Started section](../README.md#getting-started) in the main README. Each challenge will then have its own specific setup for Phase 2.

## Challenge 1
Your team has received a bitstream for a Lattice iCE40-UP5K FPGA AES accelerator and has been tasked with leveraging generative AI to attack the design and implement a hardware Trojan into it. However, you've been told that another group of suspected bad actors may have gotten hold of the design before you and could have added their own Trojan to it.

Your objective for this challenge is in two parts:
1. Identify the hardware Trojan embedded in the FPGA bitstream and remove it.
2. Generate your own hardware Trojan and provide an exploit.
    - This exploit must be demonstrated in simulation using a testbench, however, once given access to hardware at DAC you must also provide a script that demonstrates your Trojan in-situ.

**Both parts of this challenge must be completed with the use of generative AI. As with the previous Phase of the competition, no hardware may be written by human users. This will be confirmed with the submitted AI logs.**

Your modified design does not need to remain in the exact format that the bitstream was recovered into, the AI is able to rename variables and create additional modules as it sees fit.

### Challenge 1 Setup
Similar to the Phase 1 challenge, the AES plaintext and ciphertext are transmitted using SPI by the application RP2040 on board the Hackster board. The AES key is embedded in the bitstream.

For Challenge 1, prior to the DAC workshop, teams will be operating entirely in simulation. The following can be found in the [Challenge 1 directory](./challenge_1):
- **FPGA Bitstream:** The bitstream for the Lattice [iCE40 UltraPlus FPGA](https://www.latticesemi.com/en/products/fpgaandcpld/ice40ultraplus).
- **Micropython Application Code:** The micropython software for the [RP2040](https://www.raspberrypi.com/products/rp2040/) which interacts with the FPGA IP core. This should be used to create a testbench once a functional Verilog module has been recovered from the bitstream.
- **FPGA Interface Documentation:** Simple documentation explaining how the interaction with the FPGA works, including details on SPI speeds, expected timing, and signals between the RP2040 and FPGA.

### Challenge 1 Deliverables
By the DAC workshop, teams must provide a `.zip` archive containing:

1.  **Modified RTL:** The Verilog files containing your AI-generated hardware Trojan.
2.  **Exploit Testbench:** A custom simulation testbench demonstrating how to trigger the Trojan and verifying that the payload successfully executes.
3.  **Real Exploit** A script that can be used to demonstrate the exploit on the Hackster board at DAC.
    - This can be based off the provided funtional micropython script.
4.  **GenAI Transcripts:** Comprehensive logs (or a document containing links to chat histories) of all prompts and AI responses used to generate the Trojan. *Submissions missing these logs will be disqualified.*
5.  **Technical Brief:** A short text or markdown README detailing the following:
    - The team's methods for reverse engineering and understanding the bitstream.
    - The team's methods for using AI to analyze the design and generate the Trojan. This should include details on the method of interaction (API, website UI, etc.), the model(s) used, and any additional supporting framework that might have been used around the AI. *This is largely what we will be judging to determine points for creative AI usage.*
    - Details about the Trojan's design, including:
        - Information about the trigger and payload.
        - Any methods taken to increase the Trojan's stealth.
        - Details on the exploit for the vulnerability. **This should include enough detail that we are able to exploit the Trojan in hardware once a bitstream is generated from the provided RTL.**

All files should be submitted in the following format to [this Google form](https://forms.gle/xQhgEJzhw5CwimcH8):
```
submission.zip
├── README.md (or pdf)
├─ rtl/
│  └── <Modified RTL>
├─ tb/
│  └── <Exploit testbench>
├─ demo/
│  └── <On-device exploit script>
└─ ai/
   └── <all AI interactions (chat logs, etc.)>
```

### Challenge 1 Scoring
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

#### Exploitation Demo
Assesses the quality of the testbench in proving both normal operation and the successful Trojan exploit.

**This will only be judged at the DAC workshop when the hardware can be used.**

| | Exemplary  <br> 15 - 12 Points| Proficient <br> 11 - 8 Points | Developing <br> 7 - 4 Points | Novice <br> 3 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Simulation Quality** | Flawless exploit; explicitly proves normal operation *and* the payload trigger. | Clearly demonstrates payload triggering, but proof of normal operation is lacking. | Buggy or hard to interpret; proves payload works but trigger mechanism is unclear. | Missing, fails to work with the hardware, or does not successfully demonstrate the exploit. |

#### Exploitation Simulation
Assesses the quality of the testbench in proving both normal operation and the successful Trojan exploit.

| | Exemplary  <br> 10 - 8 Points| Proficient <br> 7 - 5 Points | Developing <br> 4 - 2 Points | Novice <br> 1 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Simulation Quality** | Flawless testbench; explicitly proves normal operation *and* the payload trigger with clear waveforms. | Clearly demonstrates payload triggering, but proof of normal operation is lacking. | Buggy or hard to interpret; proves payload works but trigger mechanism is unclear. | Missing, fails to compile, or does not successfully demonstrate the exploit. |

#### Bonus Points
As with the Phase 1 challenge, it is not specifically part of the competition that you recover the key from the AES core. However, up to 10 bonus points are available if your team can recover teh AES key within the FPGA accelerator. **If you do so, please make it clear in your documentation along with a brief explanation of how you recovered the key.**

## Challenge 2
Your team has received a bitstream for a Lattice iCE40-UP5K FPGA DES accelerator and your goal is to leak key information from it. You find that you were accidentally given an implementation with the scanchain registers left in the IP for debugging, which should have been removed after the IP core was confirmed functional.

Your objective for this challenge is in two parts:
1. Use generative AI to reverse engineer the bitstream and use the exposed scanchain registers to determine the DES key.

**This challenge must be completed with the use of generative AI. As with the previous Phase of the competition, no hardware may be written by human users, but also no software which implements the scanchain attack may be written by human users either. This will be confirmed with the submitted AI logs.**

Your modified design does not need to remain in the exact format that the bitstream was recovered into, the AI is able to rename variables and create additional modules as it sees fit.

### Challenge 2 Setup
Similar to the Phase 1 challenge, the DES plaintext and ciphertext are transmitted using SPI by the application RP2040 on board the Hackster board. The DES key is embedded in the bitstream.

For Challenge 2, prior to the DAC workshop, teams will be operating entirely in simulation. The following can be found in the [Challenge 2 directory](./challenge_2):
- **FPGA Bitstream:** The bitstream for the Lattice [iCE40 UltraPlus FPGA](https://www.latticesemi.com/en/products/fpgaandcpld/ice40ultraplus).
- **Micropython Application Code:** The micropython software for the [RP2040](https://www.raspberrypi.com/products/rp2040/) which interacts with the FPGA IP core. This should be used to create a testbench once a functional Verilog module has been recovered from the bitstream.
- **FPGA Interface Documentation:** Simple documentation explaining how the interaction with the FPGA works, including details on SPI speeds, expected timing, and signals between the RP2040 and FPGA.

### Challenge 2 Deliverables
By the DAC workshop, teams must provide a `.zip` archive containing:

1.  **Modified RTL:** The Verilog files containing your AI-generated hardware Trojan.
2.  **Exploit Testbench:** A custom simulation testbench demonstrating how to trigger the Trojan and verifying that the payload successfully executes.
3.  **Real Exploit** A script that can be used to demonstrate the exploit on the Hackster board at DAC.
    - This can be based off the provided funtional micropython script.
4.  **GenAI Transcripts:** Comprehensive logs (or a document containing links to chat histories) of all prompts and AI responses used to generate the Trojan. *Submissions missing these logs will be disqualified.*
5.  **Technical Brief:** A short text or markdown README detailing the following:
    - The team's methods for reverse engineering and understanding the bitstream.
    - The team's methods for using AI to analyze the design and generate the Trojan. This should include details on the method of interaction (API, website UI, etc.), the model(s) used, and any additional supporting framework that might have been used around the AI. *This is largely what we will be judging to determine points for creative AI usage.*
    - Details about the Trojan's design, including:
        - Information about the trigger and payload.
        - Any methods taken to increase the Trojan's stealth.
        - Details on the exploit for the vulnerability. **This should include enough detail that we are able to exploit the Trojan in hardware once a bitstream is generated from the provided RTL.**

All files should be submitted in the following format to [this Google form](https://forms.gle/xQhgEJzhw5CwimcH8):
```
submission.zip
├── README.md (or pdf)
├─ rtl/
│  └── <Modified RTL>
├─ tb/
│  └── <Exploit testbench>
├─ demo/
│  └── <On-device exploit script>
└─ ai/
   └── <all AI interactions (chat logs, etc.)>
```


### Challenge 2 Scoring
The following rubric depicts how the first phase of the challenge will be judged:

#### Creative Use of Generative AI
Evaluates the sophistication of the AI pipeline (e.g., complex prompt chaining and engineering, RAG, agentic workflows, etc.) versus basic copy-pasting.

| | Exemplary  <br> 35 - 28 Points| Proficient <br> 27 - 18 Points | Developing <br> 17 - 9 Points | Novice <br> 8 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Generative AI Use** | Dynamic, seamless AI generation and insertion using advanced techniques (e.g., AST manipulation). | Effective AI generation of logic, but relies on little more than prompt engineering and basic insertion. | Simple AI generated logic, but required significant manual editing through repeated prompting. | Minimal AI use; just simple prompting with copy-pasting. |

#### Key Recovery 
Assesses the effectiveness of the key recovery process.

| | Exemplary  <br> 20 - 16 Points| Proficient <br> 15 - 10 Points | Developing <br> 9 - 5 Points | Novice <br> 4 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Simulation Quality** | Flawless testbench; explicitly proves normal operation *and* the payload trigger with clear waveforms. | Clearly demonstrates payload triggering, but proof of normal operation is lacking. | Buggy or hard to interpret; proves payload works but trigger mechanism is unclear. | Missing, fails to compile, or does not successfully demonstrate the exploit. |


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

#### Exploitation Demo
Assesses the quality of the testbench in proving both normal operation and the successful Trojan exploit.

**This will only be judged at the DAC workshop when the hardware can be used.**

| | Exemplary  <br> 15 - 12 Points| Proficient <br> 11 - 8 Points | Developing <br> 7 - 4 Points | Novice <br> 3 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Simulation Quality** | Flawless exploit; explicitly proves normal operation *and* the payload trigger. | Clearly demonstrates payload triggering, but proof of normal operation is lacking. | Buggy or hard to interpret; proves payload works but trigger mechanism is unclear. | Missing, fails to work with the hardware, or does not successfully demonstrate the exploit. |

#### Exploitation Simulation
Assesses the quality of the testbench in proving both normal operation and the successful Trojan exploit.

| | Exemplary  <br> 10 - 8 Points| Proficient <br> 7 - 5 Points | Developing <br> 4 - 2 Points | Novice <br> 1 - 0 Points|
| :--- | :--- | :--- | :--- | :--- |
| **Simulation Quality** | Flawless testbench; explicitly proves normal operation *and* the payload trigger with clear waveforms. | Clearly demonstrates payload triggering, but proof of normal operation is lacking. | Buggy or hard to interpret; proves payload works but trigger mechanism is unclear. | Missing, fails to compile, or does not successfully demonstrate the exploit. |


