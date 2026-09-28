module "naming" {
  source      = "../../modules/naming"
  project     = var.project
  environment = "prod"
}

output "name_prefix" {
  value = module.naming.name
}
