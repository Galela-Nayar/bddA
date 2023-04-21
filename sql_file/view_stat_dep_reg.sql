CREATE OR REPLACE VIEW stat_departement AS
    SELECT d.dep, d.libelle AS departement, 
        SUM(p.p19_pop) AS pop_2019, 
        SUM(p.p13_pop) AS pop_2013,
        SUM(p.p08_pop) AS pop_2008,
        SUM(p.nais1319) AS nais_1319,
        SUM(p.nais0813) AS nais_0813,
        SUM(p.dece1319) AS dece_1319,
        SUM(p.dece0813) AS dece_0813
    FROM departement d
    JOIN commune c ON c.dep = d.dep
    JOIN population_stat p ON p.codgeo = c.com
    GROUP BY d.dep, d.libelle;

CREATE OR REPLACE VIEW stat_region AS
    SELECT r.reg, r.libelle AS region, 
        SUM(p.p19_pop) AS pop_2019, 
        SUM(p.p13_pop) AS pop_2013,
        SUM(p.p08_pop) AS pop_2008,
        SUM(p.nais1319) AS nais_1319,
        SUM(p.nais0813) AS nais_0813,
        SUM(p.dece1319) AS dece_1319,
        SUM(p.dece0813) AS dece_0813
    FROM region r
    JOIN departement d ON d.reg = r.reg
    JOIN commune c ON c.dep = d.dep
    JOIN population_stat p ON p.codgeo = c.com
    GROUP BY r.reg, r.libelle;