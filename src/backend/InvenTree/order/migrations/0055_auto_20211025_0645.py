# Generated by Django 3.2.5 on 2021-10-25 06:45

from django.db import migrations


from order.status_codes import SalesOrderStatus


def add_shipment(apps, schema_editor):
    """
    Create a SalesOrderShipment for each existing SalesOrder instance.

    Any "allocations" are marked against that shipment.

    For each existing SalesOrder instance, we create a default SalesOrderShipment,
    and associate each SalesOrderAllocation with this shipment
    """

    Allocation = apps.get_model('order', 'salesorderallocation')
    SalesOrder = apps.get_model('order', 'salesorder')
    Shipment = apps.get_model('order', 'salesordershipment')

    n = 0

    for order in SalesOrder.objects.all():

        """
        We only create an automatic shipment for "PENDING" orders,
        as SalesOrderAllocations were historically deleted for "SHIPPED" or "CANCELLED" orders
        """

        allocations = Allocation.objects.filter(
            line__order=order
        )

        if allocations.count() == 0 and order.status != SalesOrderStatus.PENDING:  # pragma: no cover
            continue

        # Create a new Shipment instance against this order
        shipment = Shipment.objects.create(
            order=order,
        )

        if order.status == SalesOrderStatus.SHIPPED:  # pragma: no cover
            shipment.shipment_date = order.shipment_date

        shipment.save()

        # Iterate through each allocation associated with this order
        for allocation in allocations:  # pragma: no cover
            allocation.shipment = shipment
            allocation.save()

        n += 1

    if n > 0:
        print(f"\nCreated SalesOrderShipment for {n} SalesOrder instances")


def reverse_add_shipment(apps, schema_editor):  # pragma: no cover
    """
    Reverse the migration, delete and SalesOrderShipment instances
    """

    Allocation = apps.get_model('order', 'salesorderallocation')

    # First, ensure that all SalesOrderAllocation objects point to a null shipment
    for allocation in Allocation.objects.exclude(shipment=None):
        allocation.shipment = None
        allocation.save()

    SOS = apps.get_model('order', 'salesordershipment')

    n = SOS.objects.count()

    print(f"Deleting {n} SalesOrderShipment instances")

    SOS.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0054_salesorderallocation_shipment'),
    ]

    operations = [
        migrations.RunPython(
            add_shipment,
            reverse_code=reverse_add_shipment,
        )
    ]
