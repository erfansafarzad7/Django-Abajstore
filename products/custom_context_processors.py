from .models import MainCategory, Brand


def category(request):
    brands = Brand.objects.all()
    category = MainCategory.objects.filter(parent__isnull=True)
    sub_category = MainCategory.objects.filter(parent__isnull=False)
    all_categories = {}
    for cat in category:
        all_categories[cat] = []
        for s_cat in sub_category:
            if s_cat.parent.name == cat.name:
                all_categories[cat] += [s_cat, ]
    return {'all_categories': all_categories, 'brands': brands}
