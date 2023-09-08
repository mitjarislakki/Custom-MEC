from bson import ObjectId
from flask import request, jsonify
from models import EasInstance
from mongoengine import *


def create():
    try:
        body = request.get_json()
        data = EasInstance(**body)
        data.save(cascade=True, force_insert=True)
        return jsonify(data), 201
    except:
        return jsonify({'error': 'Failed to deploy EAS information.'})


def read_all():
    try:
        data = EasInstance.objects().all()
        return jsonify(data), 200
    except:
        return jsonify({'error': 'Failed to read data'}), 404


def read_one(easId):
    document = EasInstance.objects(id=easId).first()
    data = {
            'appId': str(document.appId),
            'dnaiInfos': document.dnaiInfos,
            'dnn' : document.dnn,
            'fqdnPatternList': document.fqdnPatternList,
            'internalGroupId': document.internalGroupId, 
            'snssai' : document.snssai, 
            'svcKpi': document.svcKpi
        }
    return jsonify(data), 200
    # try:
    #     document = EasInstance.objects(id=easId).first()
    #     data = {
    #         'appId': str(document.appId),
    #         'dnaiInfos': document.dnaiInfos,
    #         'dnn' : document.dnn,
    #         'fqdnPatternList': document.fqdnPatternList,
    #         'internalGroupId': document.internalGroupId, 
    #         'snssai' : document.snssai, 
    #         'svcKpi': document.svcKpi
    #     }
    #     return jsonify(data), 200
    # except:
    #     return jsonify({'error': f'Failed to read EAS instance {easId}'}), 404


def update(easId):
    try:
        data = request.get_json()
        instance = EasInstance.objects.get_or_404(id=easId)
        instance.update(**data)
        return jsonify({'message': 'EAS information updated successfully'}), 200
    except:
        return jsonify({'error': 'Failed to update data'})


def patch(easId):
    try:
        data = request.get_json()
        instance = EasInstance.objects.get_or_404(id=easId)
        instance.update_one({'_id': ObjectId(easId)}, {'$set': data})
        return jsonify({'message': 'Partially updated instance successful'}), 200
    except:
        return jsonify({'error': 'EAS update failed'})
    

def delete(easId):
    try:
        instance = EasInstance.objects.get_or_404(id=easId)
        instance.delete()
        return jsonify({'message': 'EAS deleted successfully'}), 204
    except:
        return jsonify({'error': f'Failed to delete {easId}'})
    

