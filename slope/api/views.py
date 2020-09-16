from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from slope.api.serializers import (
    SlopeSerializer, ExpertImageSerializer,
    DModelSerializer, OrderSerializer,
    OrderImageSerializer
)
from slope.models import (
    Slope, ExpertImage, OrderImage,
    Order, DModel
)


def get_slope_object(pk):
    return get_object_or_404(Slope, pk=pk)


def get_expert_image_object(pk):
    return get_object_or_404(ExpertImage, pk=pk)


def get_d_model_object(pk):
    return get_object_or_404(DModel, pk=pk)


def get_order_object(pk):
    return get_object_or_404(Order, pk=pk)


def get_order_image_object(pk):
    return get_object_or_404(OrderImage, pk=pk)


class SlopeList(APIView):
    """
    Get all slopes or create new
    """
    def get(self, request, format=None):
        slopes = Slope.objects.all().filter(is_inactive=False)
        serializer = SlopeSerializer(slopes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = SlopeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlopeDetail(APIView):
    """
    Retrieve, update or delete slope
    """
    def get(self, request, pk, format=None):
        slope = get_slope_object(pk)
        serializer = SlopeSerializer(slope)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        slope = get_slope_object(pk)
        serializer = SlopeSerializer(slope, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        slope = get_slope_object(pk)
        slope.is_inactive = True
        slope.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SlopeForceDelete(APIView):
    """
    Force delete slope
    """
    def delete(self, request, pk, format=None):
        slope = get_slope_object(pk)
        slope.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpertImageList(APIView):
    """
    Get all expert's images or upload new
    """
    def get(self, request, format=None):
        images = ExpertImage.objects.all().filter(is_inactive=False)
        serializer = ExpertImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ExpertImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpertImageDetail(APIView):
    """
    Retrieve, update or delete expert's images
    """
    def get(self, request, pk, format=None):
        image = get_expert_image_object(pk)
        serializer = ExpertImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        image = get_expert_image_object(pk)
        serializer = ExpertImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = get_expert_image_object(pk)
        image.is_inactive = True
        image.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpertImageForceDelete(APIView):
    """
    Force delete expert's image
    """
    def delete(self, request, pk, format=None):
        image = get_expert_image_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DModelList(APIView):
    """
    Get all 3d models or create new
    """
    def get(self, request, format=None):
        model = DModel.objects.all().filter(is_inactive=False)
        serializer = DModelSerializer(model, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = DModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DModelDetail(APIView):
    """
    Retrieve, update or delete 3d models
    """
    def get(self, request, pk, format=None):
        model = get_d_model_object(pk)
        serializer = DModelSerializer(model)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        model = get_d_model_object(pk)
        serializer = DModelSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        model = get_d_model_object(pk)
        model.is_inactive = True
        model.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DModelForceDelete(APIView):
    """
    Force delete 3d model
    """
    def delete(self, request, pk, format=None):
        model = get_d_model_object(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    """
    Get all order or create new
    """
    def get(self, request, format=None):
        order = Order.objects.all().filter(is_inactive=False)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    """
    Retrieve, update or delete order
    """
    def get(self, request, pk, format=None):
        order = get_order_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        order = get_order_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = get_order_object(pk)
        order.is_inactive = True
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderForceDelete(APIView):
    """
    Force delete order
    """
    def delete(self, request, pk, format=None):
        order = get_order_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderImageList(APIView):
    """
    Get all engineer's images or upload new
    """
    def get(self, request, format=None):
        images = OrderImage.objects.all().filter(is_inactive=False)
        serializer = OrderImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = OrderImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderImageDetail(APIView):
    """
    Retrieve, update or delete engineer's images
    """
    def get(self, request, pk, format=None):
        image = get_order_image_object(pk)
        serializer = OrderImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        image = get_order_image_object(pk)
        serializer = OrderImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = get_order_image_object(pk)
        image.is_inactive = True
        image.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderImageForceDelete(APIView):
    """
    Force delete engineer's image
    """
    def delete(self, request, pk, format=None):
        image = get_expert_image_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
