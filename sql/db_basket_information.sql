SELECT date_pan as purchase_date, n_article as sku, panier_v.Prix as item_price, iso as ship_country
-- SELECT *
-- SELECT count(*) -- 7784 références vendues
FROM db_lelivre_pro.panier_v
JOIN com_v ON com_v.UID=panier_v.n_com
JOIN zones ON zones.Idpays=com_v.Pays
WHERE date_pan > "2018-12-31 23:59:59" AND date_pan < "2020-01-01 00:00:00" AND etat = 4