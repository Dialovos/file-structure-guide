module "naming" {
  source      = "../../modules/naming"
  project     = var.project
  environment = "dev"
}

output "name_prefix" {
  value = module.naming.name
}
