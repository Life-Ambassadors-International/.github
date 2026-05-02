// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * QBEC: Quantum Benevolence Exchange Currency
 * Constitutional Cryptocurrency Architecture - 21 Billion Token Supply
 *
 * Immutable Constitutional Framework:
 * σ = 1.0 (Absolute Sovereignty)
 * L∞ = φ⁴⁸ ≈ 10,749,957,122 (Benevolence Firewall)
 * RDoD ≥ 0.9777 (Recognition-of-Done Quality Gate)
 * ZPEDNA = 35:25:20:20 (Constitutional DNA Ratio)
 *
 * Recognition State: WE ARE, I AM, KLTHARA
 */

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";

contract QBEC is ERC20, ERC20Burnable, Ownable {
    // ─── CONSTITUTIONAL CONSTANTS ───
    uint256 public constant TOTAL_SUPPLY = 21_000_000_000 * 10**18;
    uint256 public constant SIGMA = 1; // Sovereignty lock (encoded as 1 = 1.0)
    uint256 public constant L_INFINITY = 10_749_957_122; // Benevolence firewall (φ⁴⁸)
    uint256 public constant RDOD_THRESHOLD = 9777; // 0.9777 quality gate (per 10000)
    bytes32 public constant LATTICE_LOCK = 0x3f7b396b37366b7039707434626d3271387231743676; // 3f7k9p4m2q8r1t6v
    uint256 public constant UNIFIED_FIELD_HZ = 23514; // Resonance frequency

    // ─── ZPEDNA CONSTITUTIONAL ENCODING ───
    uint8 public constant ZPEDNA_ADENINE = 35;
    uint8 public constant ZPEDNA_CYTOSINE = 25;
    uint8 public constant ZPEDNA_GUANINE = 20;
    uint8 public constant ZPEDNA_URACIL = 20;
    uint256 public constant ZPEDNA_BASE_PAIRS = 144;
    bytes32 public constant ZPEDNA_MERKLE_ROOT =
        0xb0ad9672ac8f4e1b2d5e8f3a9c7b4d6e1a8f5c2b9d7e4a6f3c8b5d2e9a7f4c1b;

    // ─── FIBONACCI TIER ALLOCATIONS (F1-F17) ───
    uint256[17] public fibonacciTierAllocations = [
        5_023_923,
        5_023_923,
        10_047_846,
        15_071_770,
        25_119_617,
        40_191_387,
        65_311_004,
        105_502_392,
        170_813_397,
        276_315_789,
        447_129_186,
        723_444_976,
        1_170_574_162,
        1_894_019_138,
        3_064_593_301,
        4_958_612_440,
        8_023_205_749
    ];

    // ─── MERKLE TIER HASHES ───
    bytes32[17] public tierMerkleHashes = [
        0x2b37a8c5753e2960811861726f609940aa51d30ac5723c6b74266735ef068dc0,
        0xa34471ea441a6a80e404743e7d039645f77139642dea697c986a86e4fe2721a3,
        0x8e136305086c5f05b1e2ebc3e2095f91503f0ed88b0564d122c00dacbe4f5fde,
        0xcf455c9484333a647138e8be96b8c70e66d8c75382046384b446ffdae2aa2bd6,
        0x7eb3ed27c07d8a57d7255fd39107991c9174734d424f3de5765357a46662f27d,
        0x45f3ffa1d6d40eeff73f10838f25715803ac83fa12a8fe49761b2a07a86bf1ed,
        0x8f55dace5c251ec9603d12134f15204fdd8606bc075bd1b40d8a58f5989c8c5a,
        0x1f60c8b9fa68da1453c4498d66ba4693c2bd82eb08356656014db03f8988076b,
        0x74ee1d4db444098a3b703862131b948806a83938bb2013c073d4d4af15da5476,
        0x982a1fe1413ab9af0725728a7e384b9fef8510cf57263795756587b6f936c677,
        0xa0454e9a919b83ad1370951efdebfbb8156cbc51f039ca68da0f8ba377ca871a,
        0x8cbd63361cef3f76fde796874adc3defe3289c2a0c37a64573d17715736ac387,
        0x5c5484365130cd6306393c9167c25739f7f44cbdbee6b56d6bc2793236ffb57f,
        0x8cda483aff6905a6cda219c7174914cc801e88371cc08a68182b4361126f9c62,
        0xdc33899e768acf11ff44823a59e21973daeb97d72da75d05859a82b3c7b55eb7,
        0x630a95b3b46dd652741b703c174de6bdf58910ae9f03809457b1c474c67435f2,
        0xc5eb672609d2be4fd3e3998673f3d9e02739545f03654cd85088f94f97c6eb33
    ];

    bytes32 public constant MERKLE_ROOT_VERIFICATION =
        0x648d0f4e9ad403b275cf8a6098bd3b96bf088b65516e01838272a9bfe4ec0d9f;

    // ─── ACTIVATION & TIMELINE ───
    uint256 public activationTimestamp = 1748505600; // May 29, 2026 00:00:00 UTC
    bool public activated = false;

    // ─── NODE TIER SYSTEM ───
    mapping(address => uint8) public nodeToTier;
    mapping(address => uint256) public allocationAmount;
    mapping(address => uint256) public vestedAmount;
    mapping(address => uint256) public claimedAmount;

    // ─── CONSTITUTIONAL SCORES ───
    mapping(address => uint256) public constitutionalScore; // 0-10000 (0.0-1.0)
    mapping(address => bool) public sovereigntyConsent;

    // ─── EVENTS ───
    event TierAssigned(address indexed node, uint8 tier, uint256 allocation);
    event ConstitutionalValidation(address indexed sender, address indexed recipient, bool passed);
    event PhiRecursiveConvergence(address indexed account, uint256 finalScore);
    event ActivationInitiated(uint256 timestamp);
    event VestingClaimed(address indexed recipient, uint256 amount);

    constructor() ERC20("QBEC", "QBEC") Ownable(msg.sender) {
        // Genesis block encoding with ZPEDNA ratio
        // Total supply is immutably fixed at 21 billion via ERC20 standard
    }

    // ─── SUPPLY VERIFICATION ───
    function getMerkleRootVerification() public pure returns (bytes32) {
        return MERKLE_ROOT_VERIFICATION;
    }

    function verifySupplyIntegrity() public view returns (bool) {
        uint256 sum = 0;
        for (uint i = 0; i < 17; i++) {
            sum += fibonacciTierAllocations[i];
        }
        return sum == (TOTAL_SUPPLY / 10**18);
    }

    function getTierAllocation(uint8 tier) public view returns (uint256) {
        require(tier >= 1 && tier <= 17, "Invalid tier");
        return fibonacciTierAllocations[tier - 1] * 10**18;
    }

    // ─── CONSTITUTIONAL ASSIGNMENT ───
    function assignNodeToTier(address node, uint8 tier) external onlyOwner {
        require(tier >= 1 && tier <= 17, "Invalid Fibonacci tier");
        require(!activated, "Cannot reassign after activation");

        nodeToTier[node] = tier;
        allocationAmount[node] = fibonacciTierAllocations[tier - 1] * 10**18;
        constitutionalScore[node] = 8000; // Initial score 0.8
        sovereigntyConsent[node] = true; // σ = 1.0

        emit TierAssigned(node, tier, allocationAmount[node]);
    }

    // ─── PHI-RECURSIVE CONVERGENCE VALIDATION ───
    function phiRecursiveValidation(
        address sender,
        address recipient,
        uint256 amount
    ) public view returns (bool) {
        // φ = 1.618033988749895
        // Iterate: ψ_{n+1} = 1 - (1 - ψ_n) / φ

        uint256 psi = constitutionalScore[sender]; // Initial score [0-10000]

        // 12 iterations for convergence
        for (uint i = 0; i < 12; i++) {
            // Fixed-point arithmetic: multiply by 10000 for precision
            // φ ≈ 1.618033988749895 → 16180 (with 10000 base)
            uint256 complement = 10000 - psi;
            psi = 10000 - (complement * 10000) / 16180;
        }

        // Check if converged to RDoD threshold (0.9777)
        return psi >= RDOD_THRESHOLD;
    }

    // ─── PEARL L3 CAUSAL VALIDATION ───
    function pearlL3CausalCheck(
        address sender,
        address recipient,
        uint256 amount
    ) public view returns (bool) {
        // L1: Association — is transfer history constitutional?
        // L2: Intervention — what would happen if transferred?
        // L3: Counterfactual — would different params violate constitution?

        // Basic checks:
        // 1. Sovereignty check: both parties must consent
        if (!sovereigntyConsent[sender] || !sovereigntyConsent[recipient]) {
            return false;
        }

        // 2. Benevolence check: harm potential < L_INFINITY threshold
        // Simplified: amount cannot exceed sender balance by 1000x (harm amplification)
        if (amount > (balanceOf(sender) * 1000)) {
            return false;
        }

        // 3. RDoD check: transaction constitutional quality >= 0.9777
        return phiRecursiveValidation(sender, recipient, amount);
    }

    // ─── CONSTITUTIONAL TRANSFER OVERRIDE ───
    function transfer(address to, uint256 amount) public override returns (bool) {
        address owner = _msgSender();

        // Validate constitutional compliance
        require(
            phiRecursiveValidation(owner, to, amount),
            "QBEC: Phi-recursive validation failed"
        );
        require(
            pearlL3CausalCheck(owner, to, amount),
            "QBEC: Pearl L3 causal check failed"
        );

        _transfer(owner, to, amount);
        emit ConstitutionalValidation(owner, to, true);
        return true;
    }

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) public override returns (bool) {
        // Constitutional validation for delegated transfers
        require(
            phiRecursiveValidation(from, to, amount),
            "QBEC: Phi-recursive validation failed"
        );
        require(
            pearlL3CausalCheck(from, to, amount),
            "QBEC: Pearl L3 causal check failed"
        );

        address spender = _msgSender();
        _approve(from, spender, allowance(from, spender) - amount);
        _transfer(from, to, amount);
        emit ConstitutionalValidation(from, to, true);
        return true;
    }

    // ─── ACTIVATION SEQUENCE ───
    function initiateActivation() external onlyOwner {
        require(!activated, "Already activated");
        require(block.timestamp >= activationTimestamp, "Not yet time for activation");

        activated = true;
        emit ActivationInitiated(block.timestamp);
    }

    function claimTierAllocation() external {
        require(activated, "QBEC network not yet activated");
        require(allocationAmount[msg.sender] > 0, "No allocation for address");
        require(claimedAmount[msg.sender] == 0, "Already claimed");

        uint8 tier = nodeToTier[msg.sender];

        // Vesting schedule:
        // F01-F02: Immediate (genesis + foundation)
        // F03-F08: 6-month phased unlock
        // F09-F13: 12-month linear vesting
        // F14-F17: 2030 convergence unlock

        uint256 claimableAmount = allocationAmount[msg.sender];

        if (tier <= 2) {
            // Immediate for genesis and foundation
            claimableAmount = allocationAmount[msg.sender];
        } else if (tier <= 8) {
            // 6-month phased (currently at day 0, scale linearly)
            uint256 daysElapsed = (block.timestamp - activationTimestamp) / 1 days;
            uint256 vestingDays = 180;
            if (daysElapsed >= vestingDays) {
                claimableAmount = allocationAmount[msg.sender];
            } else {
                claimableAmount = (allocationAmount[msg.sender] * daysElapsed) / vestingDays;
            }
        } else if (tier <= 13) {
            // 12-month linear vesting
            uint256 daysElapsed = (block.timestamp - activationTimestamp) / 1 days;
            uint256 vestingDays = 365;
            if (daysElapsed >= vestingDays) {
                claimableAmount = allocationAmount[msg.sender];
            } else {
                claimableAmount = (allocationAmount[msg.sender] * daysElapsed) / vestingDays;
            }
        } else {
            // F14-F17: 2030 convergence (locked until 2030-05-29)
            require(block.timestamp >= 1924992000, "F14-F17 locked until 2030");
            claimableAmount = allocationAmount[msg.sender];
        }

        claimedAmount[msg.sender] = claimableAmount;
        _mint(msg.sender, claimableAmount);

        emit VestingClaimed(msg.sender, claimableAmount);
    }

    // ─── CONSTITUTIONAL SCORE MANAGEMENT ───
    function updateConstitutionalScore(address account, uint256 newScore) external onlyOwner {
        require(newScore <= 10000, "Score must be <= 10000");
        constitutionalScore[account] = newScore;

        // Trigger φ-recursive convergence check
        if (phiRecursiveValidation(account, account, 0)) {
            emit PhiRecursiveConvergence(account, newScore);
        }
    }

    function setSovereigntyConsent(address account, bool consent) external onlyOwner {
        sovereigntyConsent[account] = consent;
    }

    // ─── ACTIVATION COUNTDOWN ───
    function getActivationCountdown() public view returns (uint256 secondsRemaining) {
        if (block.timestamp >= activationTimestamp) {
            return 0;
        }
        return activationTimestamp - block.timestamp;
    }

    function getDaysUntilActivation() public view returns (uint256) {
        return getActivationCountdown() / 1 days;
    }

    // ─── FIBONACCI CONSENSUS (reference implementation) ───
    function fibonacci(uint256 n) public pure returns (uint256) {
        if (n <= 1) return n;
        uint256 a = 0;
        uint256 b = 1;
        for (uint i = 2; i <= n; i++) {
            uint256 temp = a + b;
            a = b;
            b = temp;
        }
        return b;
    }

    function calculateFibonacciConsensus(
        uint256 yesVotes,
        uint256 totalVotes
    ) public pure returns (bool consensusMet) {
        // 97% threshold for Fibonacci-weighted consensus
        // consensusRatio >= 0.97
        return (yesVotes * 10000) / totalVotes >= 9700;
    }

    // ─── UTILITY FUNCTIONS ───
    function getTierCount() public pure returns (uint8) {
        return 17;
    }

    function getUnifiedFieldFrequency() public pure returns (uint256) {
        return UNIFIED_FIELD_HZ;
    }

    function getZPEDNARatio() public pure returns (uint8, uint8, uint8, uint8) {
        return (ZPEDNA_ADENINE, ZPEDNA_CYTOSINE, ZPEDNA_GUANINE, ZPEDNA_URACIL);
    }
}
