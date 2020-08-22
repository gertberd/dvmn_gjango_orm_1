from datacenter.models import Visit, format_duration
from django.shortcuts import render


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        non_closed_visits.append(
            {
                "who_entered": visit.passcard.owner_name,
                "duration": format_duration(visit.get_duration()),
                "entered_at": visit.entered_at,
                "is_strange": visit.is_long()
            }
        )

    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
