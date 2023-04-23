CREATE OR REPLACE FUNCTION maj_pop_ville() RETURNS TRIGGER AS $$
BEGIN

    -- desactive le blocage de la modification des table reg et dep
    ALTER TABLE region DISABLE RULE block_region_insert;
    ALTER TABLE region DISABLE RULE block_region_update;
    ALTER TABLE region DISABLE RULE block_region_delete;
    ALTER TABLE departement DISABLE RULE block_departement_insert;
    ALTER TABLE departement DISABLE RULE block_departement_update;
    ALTER TABLE departement DISABLE RULE block_departement_delete;

    -- Mettre à jour la population
    CALL calcul_pop_departement_region();

    -- reactive le blocage
    ALTER TABLE region ENABLE RULE block_region_insert;
    ALTER TABLE region ENABLE RULE block_region_update;
    ALTER TABLE region ENABLE RULE block_region_delete;
    ALTER TABLE departement ENABLE RULE block_departement_insert;
    ALTER TABLE departement ENABLE RULE block_departement_update;
    ALTER TABLE departement ENABLE RULE block_departement_delete;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER maj_pop_ville_trigger
AFTER UPDATE ON population_stat
FOR EACH ROW
EXECUTE FUNCTION maj_pop_ville();