from fastapi import HTTPException, status

# 400 Bad Request
VALIDATION_ERROR = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="请求参数验证失败")
INVALID_FILE_FORMAT = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无效的文件格式")
FILE_TOO_LARGE = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件过大")

# 401 Unauthorized
INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的认证凭证", headers={"WWW-Authenticate": "Bearer"}
)

# 403 Forbidden
PERMISSION_DENIED = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="没有访问该资源的权限")

# 404 Not Found
RESOURCE_NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="请求的资源不存在")
USER_NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

# 409 Conflict
DUPLICATE_ENTRY = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="数据已存在，不允许重复创建")
USER_NAME_ALREADY_EXISTS = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户名已存在")
USER_EMAIL_ALREADY_EXISTS = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户邮箱已存在")

# 422 Unprocessable Entity
UNPROCESSABLE_ENTITY = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="请求数据格式不正确")

# 500 Internal Server Error
INTERNAL_SERVER_ERROR = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="服务器内部错误")

# 503 Service Unavailable
SERVICE_UNAVAILABLE = HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="服务暂时不可用")
