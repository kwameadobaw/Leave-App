from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def pagination(page_obj, extra_params=''):
    """Generate pagination links for a page object"""
    if not page_obj or not page_obj.has_other_pages():
        return ''
    
    html = ['<nav aria-label="Page navigation">',
            '<ul class="pagination justify-content-center">']
    
    # Previous page link
    if page_obj.has_previous():
        html.append(f'<li class="page-item"><a class="page-link" href="?page={page_obj.previous_page_number()}{extra_params}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
    else:
        html.append('<li class="page-item disabled"><a class="page-link" href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
    
    # Page number links
    for i in get_page_range(page_obj):
        if i == '...':
            html.append('<li class="page-item disabled"><a class="page-link" href="#">...</a></li>')
        elif i == page_obj.number:
            html.append(f'<li class="page-item active"><a class="page-link" href="#">{i}</a></li>')
        else:
            html.append(f'<li class="page-item"><a class="page-link" href="?page={i}{extra_params}">{i}</a></li>')
    
    # Next page link
    if page_obj.has_next():
        html.append(f'<li class="page-item"><a class="page-link" href="?page={page_obj.next_page_number()}{extra_params}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
    else:
        html.append('<li class="page-item disabled"><a class="page-link" href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
    
    html.append('</ul>')
    html.append('</nav>')
    
    return mark_safe(''.join(html))

def get_page_range(page_obj, show_first_last=True, adjacent_pages=2):
    """Generate a list of page numbers to display in pagination"""
    page_range = []
    num_pages = page_obj.paginator.num_pages
    current_page = page_obj.number
    
    # Always show first page
    if show_first_last and current_page > adjacent_pages + 2:
        page_range.append(1)
        if current_page > adjacent_pages + 3:
            page_range.append('...')
    
    # Add pages around current page
    start_page = max(1, current_page - adjacent_pages)
    end_page = min(num_pages, current_page + adjacent_pages)
    
    page_range.extend(range(start_page, end_page + 1))
    
    # Always show last page
    if show_first_last and current_page < num_pages - adjacent_pages - 1:
        if current_page < num_pages - adjacent_pages - 2:
            page_range.append('...')
        page_range.append(num_pages)
    
    return page_range