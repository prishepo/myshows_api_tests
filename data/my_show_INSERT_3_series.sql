INSERT INTO public.series
("name", photo, rating, status, review)
values('Бухта вдов', 'https://cdnrrviubnyuntopbez5.svc.cdn.yandex.net/get-kinopoisk-image/1898899/20df477e-8a1c-4cf3-8518-7873e196ab60/300x450',
 1, 'will_watch'::public."seriesstatus", NULL),
('Ничегошеньки', 'https://cdnrrviubnyuntopbez5.svc.cdn.yandex.net/get-kinopoisk-image/1704946/8997def3-7896-48c4-85db-b600eca3f983/300x450',
 1, 'watching'::public."seriesstatus", NULL),
('Голяк', 'https://cdnrrviubnyuntopbez5.svc.cdn.yandex.net/get-kinopoisk-image/10812607/b63d7300-204d-42a9-a3f8-49c02c462011/300x450',
 1, 'will_watch'::public."seriesstatus", NULL)
RETURNING *;