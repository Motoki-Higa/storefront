from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Product


def say_hello(request):
    # all() does not return object yet, but this is a query set.
    # you can chain filter(), order_by() to the query set. (i.e products.filter()),
    # but 'filtered_product = products.filter()' is still query set.
    # you need to evaluate the query set to get the actual data. (i.e list(filtered_product))

    # EXAMPLES
    # == GET ALL ==
    # products = Product.objects.all() 


    # == GET ONE (with try catch) ==
    # try:
    #   product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #   pass


    # == GET ONE (alternative to try catch) ==
    # product = Product.objects.filter(pk=0).first() # returns None


    # == FILTERING ==
    # when calling filter function, we need to pass keyword argument (aka field lookups or lookup type).
    # so filter(unit_price>20) doesn't work. Instead do filter(unit_price__gt=20)
    # -- i.e 1
    # products = Product.objects.filter(unit_price__range=(20,30))
    # -- i.e 2
    # products = Product.objects.filter(last_update__year=2021)
    # -- i.e 3
    # products = Product.objects.filter(description__isnull=True)


    # == COMPLEX FILTERING ==
    # -- i.e AND operator
    # products = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # products = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    # -- i.e OR operator: we need to use Q class (Q as in query expression)
    # products = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

    # -- i.e reference fields using F
    # products = Product.objects.filter(inventory=F('unit_price'))


    # == SORTING ==
    # -- sort by title in ascending order
    # products = Product.objects.order_by('title')

    # -- sort by title in decending order
    # products = Product.objects.order_by('-title')
    # products = Product.objects.order_by('title').reverse()

    # -- accessing earliest single item
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')

    # -- accessing latest single item
    # product = Product.objects.order_by('unit_price')[-1]
    # product = Product.objects.earliest('unit_price')


    # == LIMITING ==
    # -- 0, 1, 2, 3, 4
    # products = Product.objects.all()[:5]
    # -- 5, 6, 7, 8, 9
    # products = Product.objects.all()[5:10]


    # == SELECTING FIELDS TO QUERY ==
    # -- standard query
    # products = Product.objects.values('id', 'title')
    # -- query related field by using double underscore
    # products = Product.objects.values('id', 'title', 'description', 'collection__title')


    # == SELECTING RELATED OBJECTS == (preload related objects)
    # -- use select_related() when other end of relationship has ONE object
    products = Product.objects.select_related('collection').all()
    # -- use prefetch_related() when other end of relationship has MANY object
    # products = Product.objects.prefetch_related('promotions').all()


    # == AGGREGATING OBJECTS ==
    # -- Count -- 
    # count=Count('pk') is renaming the key name to count, 
    # otherwise you can do like this aggregate(count=Count('pk')), but this returns pk__count as key
    # results = Product.objects.aggregate(count=Count('pk'))
    # combine with other aggregation
    results = Product.objects.aggregate(count=Count('pk'), min_price=Min('unit_price'))


    return render(request, 'hello.html', {
      'name': 'Motoki',
      'products': list(products),
      'results': results
    })
