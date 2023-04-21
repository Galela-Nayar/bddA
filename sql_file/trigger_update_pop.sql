CREATE OR REPLACE FUNCTION maj_pop_ville() RETURNS TRIGGER AS $$
BEGIN

    -- desactive le blocage de la modification des table reg et dep
    ALTER TABLE regitons DISABLE RULE block_regions_insert;
    ALTER TABLE regions DISABLE RULE block_regions_update;
    ALTER TABLE regions DISABLE RULE block_regions_delete;
    ALTER TABLE departements DISABLE RULE block_departements_insert;
    ALTER TABLE departements DISABLE RULE block_departements_update;
    ALTER TABLE departements DISABLE RULE block_departements_delete;

    -- Mettre à jour la population
    CALL calcul_pop_departement_region();

    -- reactive le blocage
    ALTER TABLE regions ENABLE RULE block_regions_insert;
    ALTER TABLE regions ENABLE RULE block_regions_update;
    ALTER TABLE regions ENABLE RULE block_regions_delete;
    ALTER TABLE departements ENABLE RULE block_departements_insert;
    ALTER TABLE departements ENABLE RULE block_departements_update;
    ALTER TABLE departements ENABLE RULE block_departements_delete;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER maj_pop_ville_trigger
AFTER UPDATE ON population_stat
FOR EACH ROW
EXECUTE FUNCTION maj_pop_ville();