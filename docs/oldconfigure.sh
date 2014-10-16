
	./create_default_user.sh
	keystone/create_user.sh keystone ${HOST_NAME}
	keystone/register_service.sh keystone ${HOST_NAME}
	glance/create_user.sh glance ${HOST_NAME}
	glance/register_service.sh glance ${HOST_NAME}
	nova/create_user.sh nova ${HOST_NAME}
	nova/register_service.sh nova ${HOST_NAME}
	./keystone_test.sh ${HOST_NAME}
	./glance_test.sh ${HOST_NAME}

