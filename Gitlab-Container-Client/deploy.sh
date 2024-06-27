#!/bin/sh

# Deploy ECS Fargate cloudformation (or whatever)
aws cloudformation deploy --template-file template.yaml --stack-name my-fargate-stack --capabilities CAPABILITY_NAMED_IAM
