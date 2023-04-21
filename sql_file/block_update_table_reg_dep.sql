-- Bloquer toutes les modifications sur la table REGION
CREATE RULE block_regions_insert AS ON INSERT TO region DO INSTEAD NOTHING;
CREATE RULE block_regions_update AS ON UPDATE TO region DO INSTEAD NOTHING;
CREATE RULE block_regions_delete AS ON DELETE TO region DO INSTEAD NOTHING;

-- Bloquer toutes les modifications sur la table DEPARTEMENT
CREATE RULE block_departements_insert AS ON INSERT TO departement DO INSTEAD NOTHING;
CREATE RULE block_departements_update AS ON UPDATE TO departement DO INSTEAD NOTHING;
CREATE RULE block_departements_delete AS ON DELETE TO departement DO INSTEAD NOTHING;