from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from eveuniverse.models import EveSolarSystem
from .forms import TargetForm, TargetUpdateForm
from .models import Target


def _can_edit(user, target: Target) -> bool:
    if not user.is_authenticated:
        return False
    if user.has_perm("aa_targetboard.change_target"):
        return True
    return target.created_by_id == getattr(user, "id", None)


def _can_delete(user, target: Target) -> bool:
    return user.is_authenticated and user.has_perm("aa_targetboard.delete_target")


@login_required
def solar_system_search(request):
    q = request.GET.get("q", "").strip()
    results = []
    if len(q) >= 2:
        systems = EveSolarSystem.objects.filter(name__icontains=q).order_by("name")[:20]
        results = [{"id": s.id, "text": s.name} for s in systems]
    return JsonResponse({"results": results})


@login_required
@permission_required("aa_targetboard.view_target", raise_exception=True)
def target_list(request):
    qs = Target.objects.select_related("solar_system")

    # ---- filters (unchanged) ----
    status = request.GET.get("status", "").strip()
    objective = request.GET.get("objective", "").strip()
    target_type = request.GET.get("type", "").strip()
    search = request.GET.get("q", "").strip()

    if status:
        qs = qs.filter(status=status)
    if objective:
        qs = qs.filter(objective=objective)
    if target_type:
        qs = qs.filter(target_type=target_type)
    if search:
        qs = qs.filter(
            Q(title__icontains=search)
            | Q(solar_system__name__icontains=search)
            | Q(structure_name__icontains=search)
            | Q(notes__icontains=search)
        )

    # ---- sorting (NEW) ----
    order = request.GET.get("order", "-updated_at").strip()

    allowed_orders = {
        "title", "-title",
        "solar_system__name", "-solar_system__name",
        "structure_name", "-structure_name",
        "target_type", "-target_type",
        "objective", "-objective",
        "priority", "-priority",
        "status", "-status",
        "timer_start", "-timer_start",
        "timer_final", "-timer_final",
        "created_at", "-created_at",
        "updated_at", "-updated_at",
    }
    if order not in allowed_orders:
        order = "-updated_at"

    qs = qs.order_by(order)

    # ---- pagination (NEW) ----
    page_size = 50  # adjust to taste
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "targets": page_obj.object_list,
        "page_obj": page_obj,
        "paginator": paginator,
        "order": order,
        "filters": {
            "status": status,
            "objective": objective,
            "type": target_type,
            "q": search,
        },
        "choices": {
            "status": Target.Status.choices,
            "objective": Target.Objective.choices,
            "type": Target.TargetType.choices,
        },
        # helpful for templates to preserve querystring when clicking sort links
        "qs_params": request.GET.copy(),
    }
    return render(request, "aa_targetboard/target_list.html", context)
@login_required
@permission_required("aa_targetboard.add_target", raise_exception=True)
def target_create(request):
    if request.method == "POST":
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.save(commit=False)
            target.created_by = request.user
            target.save()
            messages.success(request, "Target created.")
            return redirect("aa_targetboard:detail", pk=target.pk)
    else:
        form = TargetForm()

    return render(request, "aa_targetboard/target_form.html", {"form": form, "mode": "create"})


@login_required
@permission_required("aa_targetboard.view_target", raise_exception=True)
def target_detail(request, pk: int):
    target = get_object_or_404(Target, pk=pk)

    update_form = TargetUpdateForm()
    if request.method == "POST":
        # posting an update/comment
        if not request.user.has_perm("aa_targetboard.view_target"):
            raise Http404()
        update_form = TargetUpdateForm(request.POST)
        if update_form.is_valid():
            upd = update_form.save(commit=False)
            upd.target = target
            upd.created_by = request.user
            upd.save()
            messages.success(request, "Update posted.")
            return redirect("aa_targetboard:detail", pk=target.pk)

    context = {
        "target": target,
        "updates": target.updates.all(),
        "update_form": update_form,
        "can_edit": _can_edit(request.user, target),
        "can_delete": _can_delete(request.user, target),
    }
    return render(request, "aa_targetboard/target_detail.html", context)


@login_required
@permission_required("aa_targetboard.change_target", raise_exception=True)
def target_edit(request, pk: int):
    target = get_object_or_404(Target, pk=pk)
    if not _can_edit(request.user, target):
        raise Http404()

    if request.method == "POST":
        form = TargetForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            messages.success(request, "Target updated.")
            return redirect("aa_targetboard:detail", pk=target.pk)
    else:
        form = TargetForm(instance=target)

    return render(request, "aa_targetboard/target_form.html", {"form": form, "mode": "edit", "target": target})


@login_required
@permission_required("aa_targetboard.delete_target", raise_exception=True)
def target_delete(request, pk: int):
    target = get_object_or_404(Target, pk=pk)
    if request.method == "POST":
        target.delete()
        messages.success(request, "Target deleted.")
        return redirect("aa_targetboard:list")
    return render(request, "aa_targetboard/target_delete.html", {"target": target})
