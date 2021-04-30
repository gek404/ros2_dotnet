// generated from rosidl_generator_cs/resource/msg_typesupport.c.em
// generated code does not contain a copyright notice

@#######################################################################
@# EmPy template for generating <msg_pkg>_s.ep.<typesupport_impl>_c.c files
@#
@# Context:
@#  - package_name
@#  - interface_path
@#  - include_parts
@#  - message (IdlMessage structure)
@#######################################################################
@

@{
from rosidl_generator_c import idl_structure_type_to_c_typename
}

#include <stdbool.h>
#include <stdint.h>
#include <rosidl_runtime_c/message_type_support_struct.h>
#include <rosidl_runtime_c/visibility_control.h>


@{
msg_typename = idl_structure_type_to_c_typename(message.structure.namespaced_type)
key = "/".join(include_parts)
parts_for_path = include_parts[:-1]
parts_for_path.append('detail')
parts_for_path.append(include_parts[-1])
include_path_2 = "/".join(parts_for_path)
includes = {}
includes[key + '_support'] = '#include <%s__type_support.h>' % include_path_2
includes[key + '_struct'] = '#include <%s__struct.h>' % include_path_2
includes[key + '_functions'] = '#include <%s__functions.h>' % include_path_2
}@
@[for v in sorted(includes.values())]@
@(v)
@[end for]@

ROSIDL_GENERATOR_C_EXPORT
void * @(msg_typename)_native_get_type_support()
{
    return (void *)ROSIDL_GET_MSG_TYPE_SUPPORT(@(package_name), @(include_parts[1]), @(message.structure.namespaced_type.name));
}

ROSIDL_GENERATOR_C_EXPORT
void *@(msg_typename)_native_create_native_message()
{
   @(msg_typename) *ros_message = @(msg_typename)__create();
   return ros_message;
}

ROSIDL_GENERATOR_C_EXPORT
void @(msg_typename)_native_destroy_native_message(void *raw_ros_message) {
  @(msg_typename) *ros_message = (@(msg_typename) *)raw_ros_message;
  @(msg_typename)__destroy(ros_message);
}
