## Configuration Example

```yaml
# one.yaml
images:
  terraform: dnxsolutions/terraform:0.13.0-dnx1
  gsuite: dnxsolutions/aws-google-auth:latest
  azure: dnxsolutions/docker-aws-azure-ad:latest
  aws: dnxsolutions/aws:1.18.44-dnx2
  aws_2: dnxsolutions/aws:2.0.37-dnx1
  ecs_deploy: dnxsolutions/ecs-deploy:1.2.0

required_version: ">= 0.5.0, <= 0.7.0"

# ECS App
app:
  name: copacabana
  port: 80
  docker:
    file: Dockerfile
    image_name: copacabana
    registry_type: ecr
    registry_options:
      ecr_aws_account_id: <redact>
      ecr_aws_region: ap-southeast-2
      ecr_aws_assume_role: true
      ecr_aws_role: <redact>
  ecs_task_definition_file: task-definition.tpl.json

# Static App
app:
  type: static
  src: ./build
  s3_bucket_name: <redact>
  distribution_id: <redact>

workspaces:

  # ECS App example:
  mgmt_ecs_app:
    type: ecs
    aws:
      account_id: <redact>
      role: <redact>
      assume_role: true|false (default to false)
      region: ap-southeast-2
    ecs_cluster_name: cluster-01

  # Static App example:
  mgmt_static_app:
    aws:
      account_id: <redact>
      role: <redact>
      region: ap-southeast-2
      assume_role: true
    # Override the template static app
    app:
      src: ./build
      s3_bucket_name: <redact>
      distribution_id: <redact>

  # Terraform example
  mgmt:
    aws:
      account_id: <redact>
      role: <redact>
  nonprod:
    aws:
      account_id: <redact>
      role: <redact>
  prod:
    aws:
      account_id: <redact>
      role: <redact>
  default:
    aws:
      account_id: <redact>
      role: <redact>
      assume_role: true|false (default to false)
```