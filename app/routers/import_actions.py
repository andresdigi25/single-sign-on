from io import StringIO
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Path, Depends
from app.services import auth as auth_service, users as user_service

from app.models.responses import generic_responses_2
from app.models.users import ImportUsersResponse, ImportUserStatusResponse, ImportUsersResponse2

router = APIRouter()


@router.post(
    '/cognito/job_import',
    include_in_schema=False,
    status_code=201,
    response_model=ImportUsersResponse,
    responses=generic_responses_2,
    dependencies=[Depends(auth_service.api_key_protected)]
)
async def cognito_job_import_users(csv_file: UploadFile = File(...)):
    """
        Import multiples users from a local CSV file:

        ### Authentication: `x-api-key`

        ### File:
        - **csv_file**: required a CSV file from your local
    """

    if csv_file.content_type != 'text/csv':
        raise HTTPException(400, detail='Invalid document type')

    if not csv_file.filename.endswith('.csv'):
        raise HTTPException(400, detail='Invalid file extension')

    csv_file_bytes = await csv_file.read()

    with StringIO(csv_file_bytes.decode()) as buffer:
        user_import_job = user_service.cognito_job_import_users_from_csv(buffer).get('UserImportJob', {})

        return {
            'job_id': user_import_job.get('JobId')
        }


@router.get(
    '/cognito/job_import/status',
    include_in_schema=False,
    status_code=201,
    response_model=List[ImportUserStatusResponse],
    responses=generic_responses_2,
    dependencies=[Depends(auth_service.api_key_protected)]
)
async def cognito_job_import_status():
    """
        Get the status for the import job:

        ### Authentication: `x-api-key`
    """

    job_status = user_service.import_users_status()
    items = [{
        'status': i.get('Status'),
        'start_date': i.get('StartDate'),
        'end_date': i.get('CompletionDate'),
        'imported_users': i.get('ImportedUsers'),
        'skipped_users': i.get('SkippedUsers'),
        'failed_users': i.get('FailedUsers'),
        'message': i.get('CompletionMessage')
    } for i in job_status]

    return items


@router.post(
    '/import',
    status_code=201,
    response_model=ImportUsersResponse2,
    responses=generic_responses_2,
    dependencies=[Depends(auth_service.api_key_protected)]
)
async def import_users(csv_file: UploadFile = File(...)):
    """
        Import multiples users from a local CSV file:

        ### Authentication: `x-api-key`

        ### File:
        - **csv_file**: required a CSV file from your local
    """

    if csv_file.content_type != 'text/csv':
        raise HTTPException(400, detail='Invalid document type')

    if not csv_file.filename.endswith('.csv'):
        raise HTTPException(400, detail='Invalid file extension')

    csv_file_bytes = await csv_file.read()

    with StringIO(csv_file_bytes.decode()) as buffer:
        success, failed = user_service.import_users_from_csv(buffer)

        return {
            'imported_users': success,
            'failed_users': failed
        }
