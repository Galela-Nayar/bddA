CREATE OR REPLACE VIEW population_departement AS
    SELECT d.dep, d.libelle AS departement, 
        SUM(p.p19_pop) AS pop_2019, 
        SUM(p.p13_pop) AS pop_2013,
        SUM(p.p08_pop) AS pop_2008
    FROM departement d
    JOIN commune c ON c.dep = d.dep
    JOIN population_stat p ON p.codgeo = c.com
    WHERE p.codgeo IN (SELECT com FROM commune WHERE dep = d.dep)
    GROUP BY d.dep, d.libelle;


CREATE OR REPLACE VIEW population_region AS
    SELECT r.reg, r.libelle AS region, 
        SUM(p.p19_pop) AS pop_2019, 
        SUM(p.p13_pop) AS pop_2013,
        SUM(p.p08_pop) AS pop_2008
    FROM region r
    JOIN departement d ON d.reg = r.reg
    JOIN commune c ON c.dep = d.dep
    JOIN population_stat p ON p.codgeo = c.com
    WHERE p.codgeo IN (SELECT com FROM commune WHERE dep IN (SELECT dep FROM departement WHERE reg = r.reg))
    GROUP BY r.reg, r.libelle;