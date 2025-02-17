# Copyright 2016 Open Source Robotics Foundation, Inc.
# Copyright 2016-2018 Esteve Fernandez <esteve@apache.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
find_package(rmw_implementation_cmake REQUIRED)

macro(accumulate_typesupports)
  set(_typesupport_impl "")
  if(${rmw_implementation}_FOUND)
    get_rmw_typesupport(_typesupport_impl ${rmw_implementation} LANGUAGE "C")
    list_append_unique(_typesupport_impls ${_typesupport_impl})
  endif()
endmacro()

macro(rosidl_generator_cs_get_typesupports TYPESUPPORT_IMPLS)
  set(TYPESUPPORT_IMPLS "")
  set(_typesupport_impls "")
  #message("rosidl_generator_cs_get_typesupports")
  call_for_each_rmw_implementation(accumulate_typesupports)
  foreach(_typesupport_impl ${_typesupport_impls})
    message("rosidl_generator_cs_get_typesupports ${_typesupport_impl}")
    list_append_unique(TYPESUPPORT_IMPLS ${_typesupport_impl})
  endforeach()
endmacro()
