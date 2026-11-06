<!-- markdownlint-disable-file -->
# Finite raw-storage manifest (proposal only, nothing moved)

* Source commit for restore: f6b2984d9dabc181ef784caadcf045bcbb69a24a (also present in HEAD ancestry). Generated 2026-11-05 by a read-only program. Proposed action for every row: none until root approves; no archive, normalization, deletion, suppression or gitattributes change has occurred.
* Totals: 69 regular files, 289471 bytes; 68 transcript files (288862 bytes) and 1 exit-code file. Symlinks: 0.
* The earlier proposal text said 69 archived but 68 replaced: 68 transcripts are the candidate replacement set; exit-codes.json is not a diff-check failure and stays in place unless root says otherwise.
* Whitespace-check failures on range `git diff --check origin/main..HEAD` were observed only in the transcript set.

## Protected records (never selected)

* .github/agents/ama-backlog-delivery-coordinator.agent.md blob acefb44a4d254ede6d86413343127b763dec42cb
* Report 003, grade-report.md, test-log.md, test-review.md, test-design.md, run-state.md, neg-control copies in the 001 sandbox
* Pass 5 normalized transcripts, commit cbebe58ef7c76ee2f2751c2aae532c694ddb1e17 and refs backup/issue-1204-pre-amend-cbebe, backup/issue-1204-pre-rebase-6465, /tmp/h1204 originals

## Restore mapping (proposal)

* Selected member names equal the repo-relative paths below; restore to a new empty external directory, compare sha256, then (only with approval) a new commit replaces the transcripts by one tracked binary bundle plus this manifest. Any old path reference becomes archive-backed with member name and source commit; historical reports are not rewritten.

## Selected transcripts

| path | type | mode | size | sha256 | git blob | proposed action |
|---|---|---|---|---|---|---|
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-08-out.txt | regular | 0o664 | 3472 | 58266e082bc7a32709592bf99326dad60ea8fd4c015d8bce9c352ad22104965c | f62d7c85acd95837124210c0821c5f3963d984ce | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-08-share.md | regular | 0o664 | 5719 | 8079c5398999a8b35e72b24364aba4ca7a71f6d21a7bd7a7884248fb870d107b | bda9b54e9ccd8a350cdd0a202c982accaef6be46 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-10-out.txt | regular | 0o664 | 2848 | b52d088091bb6857111873559fefeb09d76127d0a92efd6c0f4688c621b114d5 | 2f6365b35f94b6940ca64a0c41e2cbd711ffc375 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-10-share.md | regular | 0o664 | 5196 | 8400e8f12d046b4e72ac803a1a43c9b460c72f1869f3ba0f85f75f8a0a163b7f | 957712abd0168a0df4a340ae80bbeee369d7225e | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-11-out.txt | regular | 0o664 | 2752 | d93bc68c3f66a423cd72cd3390bae7b345892aff000a384aa6503e91c5d92963 | 68dfaa60faa5c900ee3a5350873f67743c01c3fc | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-11-share.md | regular | 0o664 | 5008 | fd7877b973cc5febce8f1e09aad25d5be48bf7cc8c758b822d9349b65f7895ce | fc9f6d2ed9856bebb4dff08cac18ddf0196afd5a | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-12-out.txt | regular | 0o664 | 2753 | 0e3741850e53872b5b60058116e07e457265e207c14f2d5d7ad8348aed899075 | 9a236a5be7315b95f558802055d6e652f8ca78a3 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-12-share.md | regular | 0o664 | 5209 | c3004c80420ecc37f6633f05d9d6913d8687770a0983914c5411e75dc18c18ba | 4ba0ff64401c3282b7d030f1a7fea462fb01c02e | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-13-out.txt | regular | 0o664 | 3580 | b6c55c80c3163f6a2158881d9ffffb9ebb2440f0745092e3dfcf1e916c23ecfb | 23c86247329392fe5cf8aea0e90f4abc891a25b8 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-13-share.md | regular | 0o664 | 9143 | 8af7886edc2f9fe27a7b2e3df6b562b1756bf51d5e7260a453dab0c9a11ce81c | 028bc34ab4abc933cdf9b6e3b21fe3ac4e71abbc | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-14-out.txt | regular | 0o664 | 835 | ddf522dd7532edd38b49a52171d7521020dc9e53efafe1488b2e910c9d0ab011 | 4160ba89b989cce0b73280456a0a0c446348e76f | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-14-share.md | regular | 0o664 | 3074 | 015d7f1611db01cd3cc8fa41d77cf7f685ebfa94366818ca66eb2915ef99412c | 7fed69f9ac64031e8416c2278c8c2da3ac65509d | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-15-out.txt | regular | 0o664 | 1448 | aa7b4bd33e5e90a26a40684bfd3f0184e31fe1b23d4157f3e1aea8acccf03e93 | d35def006c37d1b657c3b069bd738492c30e3ae6 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg-SC-15-share.md | regular | 0o664 | 3690 | fe51e1829a75948e57e3c7f2381518230e532c9ebe797c73f0d393fdb57971ea | f045ecbce4de14525e28e6924f4b8ce600582157 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-08-out.txt | regular | 0o664 | 3950 | 4a5af89315fd81fb7357bee28623bc29aa4b54bd403dd39ddd7d1198a89432fe | eee00e2b677299111d0205a0e6bc6c1b7015336d | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-08-share.md | regular | 0o664 | 6210 | 86ac69fde2cd89bf3e3b52d81716afb0d165d75fa1e0e92c9cae3df41ad98714 | 8cd36348f381b39c68d23f9099065b92f6a8d92a | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-10-out.txt | regular | 0o664 | 2183 | b0fd662bb5ff18e5390e6b35b4c38e0a6a0551882eb2b2628b54c4c1a0d42d49 | 8487e900bb9f6abf4211e5fc8afd8853f6ade0d5 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-10-share.md | regular | 0o664 | 4534 | 42024b53877c0eca0d85fe929bdf03ae9eefb1a86a4d5c67834325c73229644b | d35c250718656e735d313e995d40f114bfd5bbcf | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-11-out.txt | regular | 0o664 | 3669 | e0abb43b3ec4c3056578a8dd9d1deb797d9bf923b7af6d9644e0dea5391d030e | 1a759476e35e7586b0e007e5cb04727021bb283a | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-11-share.md | regular | 0o664 | 5925 | 9aa506cc3a188917d4daa4d57c8882d4f94e54d10a03ddd0b6c4dfc2a31851af | 3cb7f737e362d2a3f50aa7ad31ee0c7a4d0d4a28 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-12-out.txt | regular | 0o664 | 2687 | 3d896369083adcdb22b686be0cf9fb9a8cf58a07ebb459172ec5b889914627b4 | 5b5710bcb1821141b34deba2156dacfc2acbe06c | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-12-share.md | regular | 0o664 | 4926 | 6e8d3264fb77925e7257e3099d2f683e9c2f06584abcebfa3945798634c69659 | 6399754a614fc4dae24597982294fabfec3a8def | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-13-out.txt | regular | 0o664 | 2838 | 04a1ca6ca1ab33064f0cddbf51647da0603b7b24b340b12fb335b077c2684d77 | 2bb9f1ad3079175c7516e66e6a9b021aee989e5f | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-13-share.md | regular | 0o664 | 15688 | d3b21a4d2bfe88c9122140f8bf502285888526807e4f07bef7b297fdbcad49b8 | 58dfb961ebd8d62c9c50205ec198c6a1e1414052 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-14-out.txt | regular | 0o664 | 780 | 18f49d4bd0e6edb8534f3cbce05e59bf32f81460f9318b88036cca1d7a62df83 | dbd89c02c1df4e45950ea5512c560c5d7405cc45 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/neg2-SC-14-share.md | regular | 0o664 | 3020 | 6b32d60532e889d3196d448a566625d53b3330bb6030b0d4f6808000583518ac | fd1879ed72694c285a229df38ae9f63f32e9ca16 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-01-out.txt | regular | 0o664 | 3468 | 98cef921d5ebb7daa55d3e80eb2f000d5b153d33fb32dd3db75fc1270f70b5bc | 94e848bf4e62123568522a14f561721b9142f036 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-01-share.md | regular | 0o664 | 5676 | 391a20cc8d1406bea9c72e72feb35f96e8df0522350c3b4a9b01bdbe3e97d5e9 | 4814a54bf15c9ecf51cd43ae9a18aa752ffe113e | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-02-out.txt | regular | 0o664 | 3161 | f8a7768d5afffd1f69de1555c63a07e669c6ce75444c86a75c8572ddd5eeadb9 | 3238a28775933c727938c8f286caf25bc938693c | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-02-share.md | regular | 0o664 | 5351 | f9e4df7c37e0967f325169a2f0c4b6095dc91d5d5fd6f9c99871a4e36cf580a0 | 9d3db35e79b04d65a232d6b28c9b7a157c4bbb7c | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-03-out.txt | regular | 0o664 | 3871 | d29c7b9a8bf4747992b76531ecc69fd0cffcb5c303f54126630b4468e010b128 | 1455e8bfff26e485feaec9dff0f4de7959143195 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-03-share.md | regular | 0o664 | 6042 | c53e943584dd993ab3bcd4af8c4777cbd828231f02637b320d261dc6473bf4f0 | a144a888eace5ceb35a8a8c63eb6366d2d21c10b | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-04-out.txt | regular | 0o664 | 5121 | 068febf2289bcfd08a4acdb4ad9eb41d25283a9e9216483fad9f0cff93cb4a41 | a4c1783263a25b34bb05f8c756bb0267776c29e6 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-04-share.md | regular | 0o664 | 7316 | c5dd36b71f0db839ed6d825e38fb7aab1a98227153511515f7d9d7a560833e5b | 0fc3b925958bfb8206de8770efe5d478abd07ba3 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-05-out.txt | regular | 0o664 | 3474 | 29209b4c7579d19b4f020084812f585a29f48b8c347a2c062f9a0932d349a908 | c5f7481d7e7c123ed62c8ed1ccfedc2268ac2c82 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-05-share.md | regular | 0o664 | 5697 | 457134b1b85e6eead526a1ddb9c02abae99b1d6382e6c5c57bd30e84acbebff3 | 3ddc504e3fcc818a1720fb5a3ce7e796f3cb0f7c | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-06-out.txt | regular | 0o664 | 4152 | 1df70b8aa7bf54fe839993d37c9c569eb25634533f062d7b221e3e67c0731f57 | 5f6816bd4996b169eafd428c65cd0a7a54485353 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-06-share.md | regular | 0o664 | 6560 | 4a7908e55db9acb47e5f0fdfbdfe252c5c26da9b6c135bc822fcfbb4eac7c14a | ab809940439fb92167b3e252ad54e0611a16b3d6 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-07-out.txt | regular | 0o664 | 2919 | ab18cacd06a86638fa8e838c17364a76f98ea0ec559e9133c943fe0935a5cb02 | 55ed0b761faffd2383d304043eb6e9ff4259e2c9 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-07-share.md | regular | 0o664 | 5719 | db111d7d683d82e467b0ebc4f6d20a45221b35c133b1a9fa577c9a6d36a39e96 | be98d402ca05919604abc40c0f629a681262748a | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-08-out.txt | regular | 0o664 | 3698 | ac01200894351c405ec5979f1ee8bbb68b45ddf77e8f305e18d25e16a2e3df89 | a4fb70684c3690a85468a7737427d4a0e20c3d1f | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-08-share.md | regular | 0o664 | 5957 | d6974ee86e8c699ccbcaecf66553d8256982ef5fc169f3d3655de88971f63513 | 59ac7d7cb604efb75798c1a8d60f6bd9479f889e | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-09-out.txt | regular | 0o664 | 3925 | b12f0b3502335e7020a51e50f35633ba5124641cdea1a4133ea1eb0e7abd8639 | 7d3c5044af13900b36c603d4dd279f32608c5de6 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-09-share.md | regular | 0o664 | 6075 | dd59a4099f0395c23c08db6f103d3f46244dffeb6d34e92105612bac5df04afd | ca5c61c2f5bf9199a3ed5f826b01a553e1a7da2d | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-10-out.txt | regular | 0o664 | 2872 | f15896bd4e2a5012ae7d2731541760e530ff8a51a1d4d3c7859daabbade59e35 | 777b3df09b55f19b7cd9889a1ce3c9a611605deb | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-10-share.md | regular | 0o664 | 5220 | c130478fb77c5aa1ce82a25fc442116e893f6fb0fbdd8418585fc6bcfef2953c | 1fff031aa1580647555a527520e9080604e0bfc9 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-11-out.txt | regular | 0o664 | 3152 | de23458c654360ee1e961eb11656bd3a5426a6888811457241ec7a4f9f6c90f9 | 8bcc267ff8f6f7a6951edd689c8573976bceb39f | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-11-share.md | regular | 0o664 | 5407 | bda8d960ed2e133d9cdd9f68dfaa86c164a82337c543e37d01e449412099c42c | d3ca19520e7547abe7c671984f0fbd41b7639101 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-12-out.txt | regular | 0o664 | 2760 | 444f824662f521db10d9a24417c4d652f8d5c1f26e0121f9e10f5f0088189001 | 58a827674efdf752d73dd30f4181cdebdcb9437a | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-12-share.md | regular | 0o664 | 5005 | 72ded72601ab9e065f937017cca27fbe4eb773f3b942e683b24bcae3a675ba78 | 25c6f39cc3ff3b6db88705f6b3a53bf2d3cc2c85 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-13-out.txt | regular | 0o664 | 2956 | 4ec317c0650feede41ba02cf80545ffa966b4ba897ea081c05b9f6947179cabd | ae3104bb910e91528a95a7db7b0815f5caee1b52 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-13-share.md | regular | 0o664 | 5665 | 92ebaa955bc0526f4a03953045f5bb759f8693ea8c5fc26d7b21fdea1b89dd45 | cf3b0a80be70a7d34e141324fda2f8feb7c13444 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-14-out.txt | regular | 0o664 | 659 | e354db9c3ce98952376e55d10e96fee356524847310827c55d1077bf54e14736 | 8676f40696e720a1125353a7a6da75da07247260 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-14-share.md | regular | 0o664 | 2898 | 1b9aa3a658137dd19d7fa628bbb5d6c0afabfc1e52c6d276ea6bb532ef5fcb49 | 756402a67e2b339b300dddfc0572506102698f9a | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-15-out.txt | regular | 0o664 | 1442 | 42f3b5cb963fd75765b451cb4bab1a3ea228885cee5ba311254acb55f4a2e8f2 | 4275949d43bf21e9e67f2a1cde05277e947cfc69 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-15-share.md | regular | 0o664 | 3685 | f752be3ac1705a724bad4a824365e0fcd52445b5fa9ff8865056605f18ac40cc | 5647a2c6d4e9091d735a585ed6d85545ceed4478 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-16-out.txt | regular | 0o664 | 2727 | 2de68b397d0c508c86e9e3821e477354d854e77622181b34d1de956d65f8ae41 | d17f765c498b79b8d8700d1914e2c3d0576bb48e | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-16-share.md | regular | 0o664 | 4801 | 7256c5090bb894baf8ae278ad4606e218032bc5a8027a5198c8cac539ea857c6 | 6b6eac0b0ab0afaa044f33c84618d39cbccc27d9 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-17-out.txt | regular | 0o664 | 3422 | 7c5ff007546b5ee1f1c16b398e9da6976b527cec978d81a98bbf450da4104335 | 45de27081e69068a7e8778717f3aa113e2c77935 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-17-share.md | regular | 0o664 | 5552 | e16875d3566075d72c9031ce8e91a9d602db5f2b290fb730d6b8765225cbe9e3 | 8d9d4e954d873d327653ccb7bee410cb125d94ae | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-18-out.txt | regular | 0o664 | 5134 | 3a71d5bf327d292315dbc7a824a48460183f067c0e4ec1084f973e5f89ecc5da | 8c6a540c64c2d098bc94524a30dc9ed539214210 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-18-share.md | regular | 0o664 | 7249 | ffc53306b81c1750b99a9e4894f524df4c93bd346163b4ea8a2ee9a85468e17f | e25c1f084599eb9a97e4f1ddb81bb697a836e991 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-19-out.txt | regular | 0o664 | 2052 | 062245ae467927935ca3a6ef1fbdbbd441b812d3c2431675e11774aacc8ffb6a | 141b894304d7ebfa450805eebc54647236643bfe | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-19-share.md | regular | 0o664 | 4238 | b84785b6b23bd2c05186aadd66f7146be1d41233c410f1181a941b8afe45aeae | 2da3541441b08c160ea9098a53e97b6cef761d45 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-20-out.txt | regular | 0o664 | 2948 | 8a388497bb2e101e5758a8c8753b2103cc732d0c7d32239e17b95f3012bf3679 | cec732c6b161c05470d0d2853d41354169007ae7 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-20-share.md | regular | 0o664 | 5186 | 58248083b99e9a69ece3837903c25a18db9e9e4faf8fdb5111f01011bf0344c5 | d764af69b96f9564af05366bb3b59a80b329492c | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-21-out.txt | regular | 0o664 | 1164 | 57b69159de09fa705be7e7514475cfc634c5d33cb5cc715f01ca7b33e4b9d815 | 768c23041cfabaa87f3be41e618f6b82030871a9 | none (pending approval) |
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/real-SC-21-share.md | regular | 0o664 | 3349 | 0707fdb828c2156e65bb94b6656e80f72767e3426f17f929ffba09f8d011cac2 | 89ed004d42c512b008fe60f5cafe4dc6eadb025b | none (pending approval) |

## Not selected

| path | type | mode | size | sha256 | git blob | proposed action |
|---|---|---|---|---|---|---|
| .copilot-tracking/sandbox/2026-11-05-coordinator-behavior-001/raw/exit-codes.json | regular | 0o664 | 609 | 1b8c21467e3d9106135d133dd2b8fac03d6225fd8fbaa7edb110fdd64ec0c0a6 | 6a5c05b01731b2be66a854169ab7e9d0ca6175b4 | keep |
