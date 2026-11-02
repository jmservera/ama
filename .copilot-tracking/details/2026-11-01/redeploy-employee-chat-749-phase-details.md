---
title: Redeploy employee chat fix from main 1a644d317, phase details
ms.date: 2026-11-01
---

Phase details are in the plan. Image: `zava-forward-api:rd749-1a644d317`, pushed digest `sha256:72dfb10326dc1e8c9c0eefe2970b6e11490847bb028d1fd6ddfbb699795e57bc`. Commands: `docker build -f src/api/Dockerfile src`, `az acr update`/`network-rule add` window, `docker push`, `az containerapp update -g ama -n <app> --image <repo>@<digest>`.
