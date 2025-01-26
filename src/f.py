import os
import yaml

def create_workflow_file():
    # Define the GitHub Actions workflow content
    workflow_content = {
        "name": "CI/CD Pipeline",
        "on": {
            "push": {
                "branches": ["main"]
            },
            "pull_request": {
                "branches": ["main"]
            }
        },
        "jobs": {
            "build": {
                "name": "Build and Test",
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Checkout Code",
                        "uses": "actions/checkout@v3"
                    },
                    {
                        "name": "Set up Node.js",
                        "uses": "actions/setup-node@v3",
                        "with": {
                            "node-version": "16"
                        }
                    },
                    {
                        "name": "Install Dependencies",
                        "run": "npm install"
                    },
                    {
                        "name": "Run Tests",
                        "run": "npm test"
                    }
                ]
            },
            "deploy": {
                "name": "Deploy to Production",
                "needs": ["build"],
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Checkout Code",
                        "uses": "actions/checkout@v3"
                    },
                    {
                        "name": "Deploy to S3 Bucket",
                        "env": {
                            "AWS_ACCESS_KEY_ID": "${{ secrets.AWS_ACCESS_KEY_ID }}",
                            "AWS_SECRET_ACCESS_KEY": "${{ secrets.AWS_SECRET_ACCESS_KEY }}",
                            "AWS_REGION": "us-east-1"
                        },
                        "run": """
                            aws s3 sync ./build s3://your-bucket-name --delete
                        """
                    }
                ]
            }
        }
    }

    # Ensure the directory for the workflow file exists
    workflows_dir = ".github/workflows"
    os.makedirs(workflows_dir, exist_ok=True)

    # Write the YAML content to the workflow file
    workflow_file_path = os.path.join(workflows_dir, "ci-cd.yml")
    with open(workflow_file_path, "w") as workflow_file:
        yaml.dump(workflow_content, workflow_file, default_flow_style=False)

    print(f"GitHub Actions workflow file created at: {workflow_file_path}")


if __name__ == "__main__":
    create_workflow_file()
