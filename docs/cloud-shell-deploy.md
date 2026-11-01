# Deploying Curbside from Cloud Shell

The agent runs on Agent Runtime (default region `us-central1`). Deploys can be run from Cloud Shell, signed in to the account that owns your project. A push to GitHub does not update the running agent.

> The original hackathon deployment ran in a temporary Qwiklabs project (the `Makefile` default `PROJECT_ID`). Always pass your own: `make deploy PROJECT_ID=<your-project> TOOLBOX_URL=...`.

`make deploy` records the engine's resource name in `deployment_metadata.json` (`remote_agent_runtime_id`, `null` until the first deploy) and updates that engine on later runs. It does not create a second one, as long as that file is present in the Cloud Shell checkout.

## One-time setup in Cloud Shell

Cloud Shell does not have the repo until someone clones it. In the Cloud Shell terminal:

```bash
gcloud config get-value account
gcloud config get-value project
cd ~
git clone https://github.com/<you>/curbside.git
cd curbside
```

Confirm the account and project are the ones you intend to deploy to. Use the `https://` clone URL. Cloud Shell does not have a laptop SSH key.

If clone asks for a password, sign in once with `gh auth login` (GitHub.com, HTTPS), then clone again.

`~/curbside` stays in the Cloud Shell home directory across sessions.

## After any change lands on main

Pull, then deploy. Run this from Cloud Shell, in the repo root:

```bash
cd ~/curbside
git pull
make deploy
```

`git pull` brings in `main`. `make deploy` runs the unit tests and, if they pass, uploads the `agent/` tree from that checkout to the engine above. The running agent changes when the command finishes, usually 5 to 10 minutes later.

If the terminal times out while the deploy is still going, check it instead of starting another one:

```bash
make status
```

Confirm the new code with:

```bash
make test-remote Q="Hello"
```

The Cloud console playground for that reasoning engine uses the same deployment.

One person deploys at a time. Pull immediately before `make deploy`, or Cloud Shell will publish whatever older files are already on that machine.

If `deployment_metadata.json` changes, commit it. Without that file, the next `make deploy` creates a new engine instead of updating this one.

## What does not update the agent

- Pushing or merging to `main` on GitHub.
- Editing files in Cloud Shell and stopping before `make deploy`.
- `bash scripts/load.sh 13121`. That replaces the BigQuery tables in `a4i_health` for the whole team. The agent reads those tables on the next request, so a data reload does not need a deploy.

A code or prompt change goes live only after `make deploy` finishes in Cloud Shell.
