INSERT INTO public.series
(id, "name", photo, rating, status, review)
values (284, 'Анатомия страсти', 'https://cdnrrviubnyuntopbez5.svc.cdn.yandex.net/get-kinopoisk-image/1898899/20df477e-8a1c-4cf3-8518-7873e196ab60/300x450',
1, 'will_watch'::public."seriesstatus", NULL)
RETURNING *;