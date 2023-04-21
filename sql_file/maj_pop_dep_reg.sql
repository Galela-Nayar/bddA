CREATE OR REPLACE PROCEDURE calcul_pop_departement_region() 
        LANGUAGE plpgsql
        AS $$
        BEGIN
        UPDATE departement d SET pop_departement = (
            SELECT SUM(p.p19_pop) FROM commune c JOIN population_stat p ON p.codgeo = c.com WHERE c.dep = d.dep
        );

        UPDATE region r SET pop_region = (
            SELECT SUM(p.p19_pop) FROM commune c JOIN population_stat p ON p.codgeo = c.com JOIN departement d ON c.dep = d.dep WHERE d.reg = r.reg
        );
        END;
        $$;