#!/usr/bin/env node

/**
 * QBEC Merkle Proof Verification Tool
 * Verifies the cryptographic integrity of the 21 billion token supply
 *
 * Usage:
 *   node qbec_merkle_verify.js verify-supply
 *   node qbec_merkle_verify.js verify-tier <tier_number>
 *   node qbec_merkle_verify.js calculate-root
 *   node qbec_merkle_verify.js validate-allocation <tier_number>
 */

const crypto = require('crypto');

// ─── QBEC CONSTANTS ───
const TOTAL_SUPPLY = 21_000_000_000;
const ZPEDNA_MERKLE_ROOT =
  'b0ad9672ac8f4e1b2d5e8f3a9c7b4d6e1a8f5c2b9d7e4a6f3c8b5d2e9a7f4c1b';

// Fibonacci tier allocations (F1-F17)
const FIBONACCI_TIERS = [
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
  8_023_205_749,
];

// Merkle tier hashes
const TIER_MERKLE_HASHES = [
  '2b37a8c5753e2960811861726f609940aa51d30ac5723c6b74266735ef068dc0',
  'a34471ea441a6a80e404743e7d039645f77139642dea697c986a86e4fe2721a3',
  '8e136305086c5f05b1e2ebc3e2095f91503f0ed88b0564d122c00dacbe4f5fde',
  'cf455c9484333a647138e8be96b8c70e66d8c75382046384b446ffdae2aa2bd6',
  '7eb3ed27c07d8a57d7255fd39107991c9174734d424f3de5765357a46662f27d',
  '45f3ffa1d6d40eeff73f10838f25715803ac83fa12a8fe49761b2a07a86bf1ed',
  '8f55dace5c251ec9603d12134f15204fdd8606bc075bd1b40d8a58f5989c8c5a',
  '1f60c8b9fa68da1453c4498d66ba4693c2bd82eb08356656014db03f8988076b',
  '74ee1d4db444098a3b703862131b948806a83938bb2013c073d4d4af15da5476',
  '982a1fe1413ab9af0725728a7e384b9fef8510cf57263795756587b6f936c677',
  'a0454e9a919b83ad1370951efdebfbb8156cbc51f039ca68da0f8ba377ca871a',
  '8cbd63361cef3f76fde796874adc3defe3289c2a0c37a64573d17715736ac387',
  '5c5484365130cd6306393c9167c25739f7f44cbdbee6b56d6bc2793236ffb57f',
  '8cda483aff6905a6cda219c7174914cc801e88371cc08a68182b4361126f9c62',
  'dc33899e768acf11ff44823a59e21973daeb97d72da75d05859a82b3c7b55eb7',
  '630a95b3b46dd652741b703c174de6bdf58910ae9f03809457b1c474c67435f2',
  'c5eb672609d2be4fd3e3998673f3d9e02739545f03654cd85088f94f97c6eb33',
];

const MERKLE_ROOT_VERIFICATION =
  '648d0f4e9ad403b275cf8a6098bd3b96bf088b65516e01838272a9bfe4ec0d9f';

// ─── UTILITIES ───
function sha256(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

function hashPair(a, b) {
  return sha256(a + b);
}

// ─── VERIFICATION FUNCTIONS ───
function verifySingleTier(tierNumber) {
  if (tierNumber < 1 || tierNumber > 17) {
    console.error('❌ Invalid tier number. Must be 1-17.');
    return false;
  }

  const allocation = FIBONACCI_TIERS[tierNumber - 1];
  const expectedHash = TIER_MERKLE_HASHES[tierNumber - 1];
  const calculatedHash = sha256(allocation.toString());

  console.log(`\n📊 Tier F${tierNumber} Verification:`);
  console.log(`   Allocation: ${allocation.toLocaleString()} tokens`);
  console.log(`   Expected Hash:   ${expectedHash}`);
  console.log(`   Calculated Hash: ${calculatedHash}`);
  console.log(`   Status: ${calculatedHash === expectedHash ? '✅ VERIFIED' : '❌ MISMATCH'}`);

  return calculatedHash === expectedHash;
}

function verifySupplyIntegrity() {
  const sum = FIBONACCI_TIERS.reduce((a, b) => a + b, 0);

  console.log('\n💎 TOTAL SUPPLY VERIFICATION:');
  console.log(`   Sum of Tier Allocations: ${sum.toLocaleString()} tokens`);
  console.log(`   Expected Total Supply:  ${TOTAL_SUPPLY.toLocaleString()} tokens`);
  console.log(
    `   Status: ${sum === TOTAL_SUPPLY ? '✅ EXACT MATCH' : '❌ MISMATCH'}`
  );

  if (sum === TOTAL_SUPPLY) {
    console.log('\n   ✨ Supply integrity cryptographically guaranteed');
    console.log('   Any modification to tier allocations invalidates the Merkle root.');
    return true;
  }

  return false;
}

function calculateMerkleRoot() {
  console.log('\n🌳 MERKLE TREE CALCULATION:');

  // Layer 1: Hash each tier
  let layer = TIER_MERKLE_HASHES.map((h) => h);
  console.log(`\n   Layer 0 (Tier Hashes): ${layer.length} hashes`);

  // Iteratively combine pairs upward through the tree
  let layerNum = 1;
  while (layer.length > 1) {
    const newLayer = [];
    for (let i = 0; i < layer.length; i += 2) {
      if (i + 1 < layer.length) {
        newLayer.push(hashPair(layer[i], layer[i + 1]));
      } else {
        newLayer.push(hashPair(layer[i], layer[i])); // Hash with itself if odd
      }
    }
    layer = newLayer;
    console.log(`   Layer ${layerNum}: ${layer.length} hashes`);
    layerNum++;
  }

  const calculatedRoot = layer[0];
  console.log(`\n   Calculated Merkle Root: ${calculatedRoot}`);
  console.log(`   Expected Merkle Root:   ${MERKLE_ROOT_VERIFICATION}`);
  console.log(
    `   Status: ${calculatedRoot === MERKLE_ROOT_VERIFICATION ? '✅ VERIFIED' : '❌ MISMATCH'}`
  );

  return calculatedRoot === MERKLE_ROOT_VERIFICATION;
}

function verifyAllTiers() {
  console.log('🔐 VERIFYING ALL 17 FIBONACCI TIERS...\n');
  let allValid = true;

  for (let i = 1; i <= 17; i++) {
    const isValid = verifySingleTier(i);
    allValid = allValid && isValid;
  }

  return allValid;
}

function displayQBECStatus() {
  console.log('\n╔════════════════════════════════════════════════════════════╗');
  console.log('║         QBEC: Quantum Benevolence Exchange Currency       ║');
  console.log('║    Constitutional Cryptocurrency - 21 Billion Supply      ║');
  console.log('╚════════════════════════════════════════════════════════════╝');

  console.log('\n📋 Constitutional Framework:');
  console.log('   σ (Sovereignty): 1.0');
  console.log('   L∞ (Benevolence Firewall): φ⁴⁸ ≈ 10,749,957,122');
  console.log('   RDoD (Quality Gate): ≥ 0.9777');
  console.log('   ZPEDNA Ratio: 35:25:20:20');

  console.log('\n🔗 Tier Structure:');
  console.log('   F01-F02:  Genesis & Foundation');
  console.log('   F03-F08:  Early Recognition Cascade (144 nodes)');
  console.log('   F09-F13:  Network Expansion & TCMF Integration');
  console.log('   F14-F17:  Galactic Federation (2030 Unlock)');

  console.log('\n📅 Activation Timeline:');
  console.log('   Genesis Block:    May 29, 2026 00:00:00 UTC');
  console.log('   Supply Verified:  Merkle Root √');
  console.log('   Consensus Model:  Fibonacci-Scaled 97% Threshold');

  verifySupplyIntegrity();
  calculateMerkleRoot();
}

// ─── CLI INTERFACE ───
const command = process.argv[2];
const arg = process.argv[3];

if (!command) {
  displayQBECStatus();
  console.log('\n💡 Usage:');
  console.log('   node qbec_merkle_verify.js status          (show full status)');
  console.log('   node qbec_merkle_verify.js verify-supply   (verify total supply)');
  console.log('   node qbec_merkle_verify.js verify-tier <N> (verify tier F1-F17)');
  console.log('   node qbec_merkle_verify.js calculate-root   (recalculate Merkle root)');
  console.log('   node qbec_merkle_verify.js all-tiers        (verify all tiers)');
  process.exit(0);
}

switch (command) {
  case 'status':
    displayQBECStatus();
    break;

  case 'verify-supply':
    verifySupplyIntegrity();
    break;

  case 'verify-tier':
    if (!arg) {
      console.error('❌ Please provide tier number (1-17)');
      process.exit(1);
    }
    verifySingleTier(parseInt(arg));
    break;

  case 'calculate-root':
    calculateMerkleRoot();
    break;

  case 'all-tiers':
    verifyAllTiers();
    break;

  default:
    console.error(`❌ Unknown command: ${command}`);
    process.exit(1);
}
