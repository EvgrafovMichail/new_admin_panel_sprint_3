QUERY_FILM_WORK = """
SELECT
   fw.id,
   fw.title,
   fw.description,
   fw.rating,
   fw.type,
   fw.updated_at,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ) as persons,
   array_agg(DISTINCT g.name) as genres
FROM film_work fw
LEFT JOIN person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN person p ON p.id = pfw.person_id
LEFT JOIN genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN genre g ON g.id = gfw.genre_id
WHERE fw.updated_at > %s
GROUP BY fw.id
ORDER BY fw.updated_at;
"""

QUERY_PERSON = """
SELECT
   fw.id,
   fw.title,
   fw.description,
   fw.rating,
   fw.type,
   MAX(p.updated_at) updated_at,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ) as persons,
   array_agg(DISTINCT g.name) as genres
FROM person p
LEFT JOIN person_film_work pfw ON pfw.person_id = p.id
LEFT JOIN film_work fw ON pfw.film_work_id = fw.id
LEFT JOIN genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN genre g ON g.id = gfw.genre_id
WHERE p.updated_at > %s
GROUP BY fw.id
ORDER BY updated_at;
"""

QUERY_GENRE = """
SELECT
   fw.id,
   fw.title,
   fw.description,
   fw.rating,
   fw.type,
   MAX(g.updated_at) updated_at,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ) as persons,
   array_agg(DISTINCT g.name) as genres
FROM genre g
LEFT JOIN genre_film_work gfw ON g.id = gfw.genre_id
LEFT JOIN film_work fw ON gfw.film_work_id = fw.id
LEFT JOIN person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN person p ON pfw.person_id = p.id
WHERE g.updated_at > %s
GROUP BY fw.id
ORDER BY updated_at;
"""


SQL_QUERIES = [QUERY_FILM_WORK, QUERY_PERSON, QUERY_GENRE]
