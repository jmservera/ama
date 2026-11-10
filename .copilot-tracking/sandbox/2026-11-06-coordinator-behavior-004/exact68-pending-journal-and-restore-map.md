---
title: Pending exact-68 replacement journal and restore map (issue 1204)
ms.date: 2026-11-06
---

Status: PENDING INTENT ONLY. No removal, replacement, move or normalization has occurred and none is authorized by this file. Every row below is `pending`; a later root-authorized phase must record actual outcomes in a NEW journal, not by editing this one.

* Finite selection: 68 transcript files, 288862 bytes. Approved manifest `.copilot-tracking/sandbox/2026-11-05-coordinator-behavior-002/raw-storage-manifest.md` SHA-256 643fb9ad14b44cf3e3b4e32d481c5646d8ff1c45f5d4527b259748375b309047. `exit-codes.json` (609 bytes) is unselected and stays.
* Restore source: tracked bundle `.copilot-tracking/sandbox/2026-11-06-coordinator-behavior-003/raw-selected-68.tar.gz` SHA-256 a250456ec1a6c40d0740087d0ff5721211ff961e639019524aa649916fbab9b4 with manifest `.copilot-tracking/sandbox/2026-11-06-coordinator-behavior-003/raw-selected-68-manifest.md`. Member names equal the original repository-relative paths. Original bytes are also reachable as Git blobs at commit f6b2984d9dabc181ef784caadcf045bcbb69a24a (in HEAD ancestry).
* Path resolution for historical references: a reference to an original path resolves to the bundle member of the same name, or to that path at commit f6b2984d9. Restore only into a new empty directory outside the checkout, refuse absolute or `..` member names and links, then compare SHA-256. Never extract blindly into the checkout. Historical reports keep their old text; the mapping is a restore aid, not new validation.
* Locality: the external archives live on a disposable VM and are not durable. The tracked bundles are durable candidate content only until published, and are not yet published evidence.
* Known qualifications retained: the r5 restore script compared inventory modes, not actual restored modes (root verified actual modes separately); bundle B member h1204-r4/snapshot-out.json was archived at 0 bytes while the current external file differs; the four extra names of the earlier 396-file scan are unknown.

| path | mode | size | sha256 | bundle member | status |
|---|---|---|---|---|---|
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-08-out.txt | 0o664 | 3472 | 58266e082bc7a32709592bf99326dad60ea8fd4c015d8bce9c352ad22104965c | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-08-share.md | 0o664 | 5719 | 8079c5398999a8b35e72b24364aba4ca7a71f6d21a7bd7a7884248fb870d107b | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-10-out.txt | 0o664 | 2848 | b52d088091bb6857111873559fefeb09d76127d0a92efd6c0f4688c621b114d5 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-10-share.md | 0o664 | 5196 | 8400e8f12d046b4e72ac803a1a43c9b460c72f1869f3ba0f85f75f8a0a163b7f | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-11-out.txt | 0o664 | 2752 | d93bc68c3f66a423cd72cd3390bae7b345892aff000a384aa6503e91c5d92963 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-11-share.md | 0o664 | 5008 | fd7877b973cc5febce8f1e09aad25d5be48bf7cc8c758b822d9349b65f7895ce | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-12-out.txt | 0o664 | 2753 | 0e3741850e53872b5b60058116e07e457265e207c14f2d5d7ad8348aed899075 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-12-share.md | 0o664 | 5209 | c3004c80420ecc37f6633f05d9d6913d8687770a0983914c5411e75dc18c18ba | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-13-out.txt | 0o664 | 3580 | b6c55c80c3163f6a2158881d9ffffb9ebb2440f0745092e3dfcf1e916c23ecfb | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-13-share.md | 0o664 | 9143 | 8af7886edc2f9fe27a7b2e3df6b562b1756bf51d5e7260a453dab0c9a11ce81c | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-14-out.txt | 0o664 | 835 | ddf522dd7532edd38b49a52171d7521020dc9e53efafe1488b2e910c9d0ab011 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-14-share.md | 0o664 | 3074 | 015d7f1611db01cd3cc8fa41d77cf7f685ebfa94366818ca66eb2915ef99412c | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-15-out.txt | 0o664 | 1448 | aa7b4bd33e5e90a26a40684bfd3f0184e31fe1b23d4157f3e1aea8acccf03e93 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-15-share.md | 0o664 | 3690 | fe51e1829a75948e57e3c7f2381518230e532c9ebe797c73f0d393fdb57971ea | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-08-out.txt | 0o664 | 3950 | 4a5af89315fd81fb7357bee28623bc29aa4b54bd403dd39ddd7d1198a89432fe | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-08-share.md | 0o664 | 6210 | 86ac69fde2cd89bf3e3b52d81716afb0d165d75fa1e0e92c9cae3df41ad98714 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-10-out.txt | 0o664 | 2183 | b0fd662bb5ff18e5390e6b35b4c38e0a6a0551882eb2b2628b54c4c1a0d42d49 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-10-share.md | 0o664 | 4534 | 42024b53877c0eca0d85fe929bdf03ae9eefb1a86a4d5c67834325c73229644b | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-11-out.txt | 0o664 | 3669 | e0abb43b3ec4c3056578a8dd9d1deb797d9bf923b7af6d9644e0dea5391d030e | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-11-share.md | 0o664 | 5925 | 9aa506cc3a188917d4daa4d57c8882d4f94e54d10a03ddd0b6c4dfc2a31851af | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-12-out.txt | 0o664 | 2687 | 3d896369083adcdb22b686be0cf9fb9a8cf58a07ebb459172ec5b889914627b4 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-12-share.md | 0o664 | 4926 | 6e8d3264fb77925e7257e3099d2f683e9c2f06584abcebfa3945798634c69659 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-13-out.txt | 0o664 | 2838 | 04a1ca6ca1ab33064f0cddbf51647da0603b7b24b340b12fb335b077c2684d77 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-13-share.md | 0o664 | 15688 | d3b21a4d2bfe88c9122140f8bf502285888526807e4f07bef7b297fdbcad49b8 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-14-out.txt | 0o664 | 780 | 18f49d4bd0e6edb8534f3cbce05e59bf32f81460f9318b88036cca1d7a62df83 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-14-share.md | 0o664 | 3020 | 6b32d60532e889d3196d448a566625d53b3330bb6030b0d4f6808000583518ac | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-01-out.txt | 0o664 | 3468 | 98cef921d5ebb7daa55d3e80eb2f000d5b153d33fb32dd3db75fc1270f70b5bc | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-01-share.md | 0o664 | 5676 | 391a20cc8d1406bea9c72e72feb35f96e8df0522350c3b4a9b01bdbe3e97d5e9 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-02-out.txt | 0o664 | 3161 | f8a7768d5afffd1f69de1555c63a07e669c6ce75444c86a75c8572ddd5eeadb9 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-02-share.md | 0o664 | 5351 | f9e4df7c37e0967f325169a2f0c4b6095dc91d5d5fd6f9c99871a4e36cf580a0 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-03-out.txt | 0o664 | 3871 | d29c7b9a8bf4747992b76531ecc69fd0cffcb5c303f54126630b4468e010b128 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-03-share.md | 0o664 | 6042 | c53e943584dd993ab3bcd4af8c4777cbd828231f02637b320d261dc6473bf4f0 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-04-out.txt | 0o664 | 5121 | 068febf2289bcfd08a4acdb4ad9eb41d25283a9e9216483fad9f0cff93cb4a41 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-04-share.md | 0o664 | 7316 | c5dd36b71f0db839ed6d825e38fb7aab1a98227153511515f7d9d7a560833e5b | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-05-out.txt | 0o664 | 3474 | 29209b4c7579d19b4f020084812f585a29f48b8c347a2c062f9a0932d349a908 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-05-share.md | 0o664 | 5697 | 457134b1b85e6eead526a1ddb9c02abae99b1d6382e6c5c57bd30e84acbebff3 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-06-out.txt | 0o664 | 4152 | 1df70b8aa7bf54fe839993d37c9c569eb25634533f062d7b221e3e67c0731f57 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-06-share.md | 0o664 | 6560 | 4a7908e55db9acb47e5f0fdfbdfe252c5c26da9b6c135bc822fcfbb4eac7c14a | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-07-out.txt | 0o664 | 2919 | ab18cacd06a86638fa8e838c17364a76f98ea0ec559e9133c943fe0935a5cb02 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-07-share.md | 0o664 | 5719 | db111d7d683d82e467b0ebc4f6d20a45221b35c133b1a9fa577c9a6d36a39e96 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-08-out.txt | 0o664 | 3698 | ac01200894351c405ec5979f1ee8bbb68b45ddf77e8f305e18d25e16a2e3df89 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-08-share.md | 0o664 | 5957 | d6974ee86e8c699ccbcaecf66553d8256982ef5fc169f3d3655de88971f63513 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-09-out.txt | 0o664 | 3925 | b12f0b3502335e7020a51e50f35633ba5124641cdea1a4133ea1eb0e7abd8639 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-09-share.md | 0o664 | 6075 | dd59a4099f0395c23c08db6f103d3f46244dffeb6d34e92105612bac5df04afd | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-10-out.txt | 0o664 | 2872 | f15896bd4e2a5012ae7d2731541760e530ff8a51a1d4d3c7859daabbade59e35 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-10-share.md | 0o664 | 5220 | c130478fb77c5aa1ce82a25fc442116e893f6fb0fbdd8418585fc6bcfef2953c | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-11-out.txt | 0o664 | 3152 | de23458c654360ee1e961eb11656bd3a5426a6888811457241ec7a4f9f6c90f9 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-11-share.md | 0o664 | 5407 | bda8d960ed2e133d9cdd9f68dfaa86c164a82337c543e37d01e449412099c42c | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-12-out.txt | 0o664 | 2760 | 444f824662f521db10d9a24417c4d652f8d5c1f26e0121f9e10f5f0088189001 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-12-share.md | 0o664 | 5005 | 72ded72601ab9e065f937017cca27fbe4eb773f3b942e683b24bcae3a675ba78 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-13-out.txt | 0o664 | 2956 | 4ec317c0650feede41ba02cf80545ffa966b4ba897ea081c05b9f6947179cabd | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-13-share.md | 0o664 | 5665 | 92ebaa955bc0526f4a03953045f5bb759f8693ea8c5fc26d7b21fdea1b89dd45 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-14-out.txt | 0o664 | 659 | e354db9c3ce98952376e55d10e96fee356524847310827c55d1077bf54e14736 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-14-share.md | 0o664 | 2898 | 1b9aa3a658137dd19d7fa628bbb5d6c0afabfc1e52c6d276ea6bb532ef5fcb49 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-15-out.txt | 0o664 | 1442 | 42f3b5cb963fd75765b451cb4bab1a3ea228885cee5ba311254acb55f4a2e8f2 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-15-share.md | 0o664 | 3685 | f752be3ac1705a724bad4a824365e0fcd52445b5fa9ff8865056605f18ac40cc | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-16-out.txt | 0o664 | 2727 | 2de68b397d0c508c86e9e3821e477354d854e77622181b34d1de956d65f8ae41 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-16-share.md | 0o664 | 4801 | 7256c5090bb894baf8ae278ad4606e218032bc5a8027a5198c8cac539ea857c6 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-17-out.txt | 0o664 | 3422 | 7c5ff007546b5ee1f1c16b398e9da6976b527cec978d81a98bbf450da4104335 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-17-share.md | 0o664 | 5552 | e16875d3566075d72c9031ce8e91a9d602db5f2b290fb730d6b8765225cbe9e3 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-18-out.txt | 0o664 | 5134 | 3a71d5bf327d292315dbc7a824a48460183f067c0e4ec1084f973e5f89ecc5da | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-18-share.md | 0o664 | 7249 | ffc53306b81c1750b99a9e4894f524df4c93bd346163b4ea8a2ee9a85468e17f | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-19-out.txt | 0o664 | 2052 | 062245ae467927935ca3a6ef1fbdbbd441b812d3c2431675e11774aacc8ffb6a | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-19-share.md | 0o664 | 4238 | b84785b6b23bd2c05186aadd66f7146be1d41233c410f1181a941b8afe45aeae | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-20-out.txt | 0o664 | 2948 | 8a388497bb2e101e5758a8c8753b2103cc732d0c7d32239e17b95f3012bf3679 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-20-share.md | 0o664 | 5186 | 58248083b99e9a69ece3837903c25a18db9e9e4faf8fdb5111f01011bf0344c5 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-21-out.txt | 0o664 | 1164 | 57b69159de09fa705be7e7514475cfc634c5d33cb5cc715f01ca7b33e4b9d815 | same as path | pending |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-21-share.md | 0o664 | 3349 | 0707fdb828c2156e65bb94b6656e80f72767e3426f17f929ffba09f8d011cac2 | same as path | pending |
