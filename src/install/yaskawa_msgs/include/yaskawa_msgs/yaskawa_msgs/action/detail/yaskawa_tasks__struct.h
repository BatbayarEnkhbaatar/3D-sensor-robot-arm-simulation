// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from yaskawa_msgs:action/YaskawaTasks.idl
// generated code does not contain a copyright notice

#ifndef YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__STRUCT_H_
#define YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/YaskawaTasks in the package yaskawa_msgs.
typedef struct yaskawa_msgs__action__YaskawaTasks_Goal
{
  int32_t task_number;
} yaskawa_msgs__action__YaskawaTasks_Goal;

// Struct for a sequence of yaskawa_msgs__action__YaskawaTasks_Goal.
typedef struct yaskawa_msgs__action__YaskawaTasks_Goal__Sequence
{
  yaskawa_msgs__action__YaskawaTasks_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yaskawa_msgs__action__YaskawaTasks_Goal__Sequence;


// Constants defined in the message

/// Struct defined in action/YaskawaTasks in the package yaskawa_msgs.
typedef struct yaskawa_msgs__action__YaskawaTasks_Result
{
  bool success;
} yaskawa_msgs__action__YaskawaTasks_Result;

// Struct for a sequence of yaskawa_msgs__action__YaskawaTasks_Result.
typedef struct yaskawa_msgs__action__YaskawaTasks_Result__Sequence
{
  yaskawa_msgs__action__YaskawaTasks_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yaskawa_msgs__action__YaskawaTasks_Result__Sequence;


// Constants defined in the message

/// Struct defined in action/YaskawaTasks in the package yaskawa_msgs.
typedef struct yaskawa_msgs__action__YaskawaTasks_Feedback
{
  int32_t percentage;
} yaskawa_msgs__action__YaskawaTasks_Feedback;

// Struct for a sequence of yaskawa_msgs__action__YaskawaTasks_Feedback.
typedef struct yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence
{
  yaskawa_msgs__action__YaskawaTasks_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "yaskawa_msgs/action/detail/yaskawa_tasks__struct.h"

/// Struct defined in action/YaskawaTasks in the package yaskawa_msgs.
typedef struct yaskawa_msgs__action__YaskawaTasks_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  yaskawa_msgs__action__YaskawaTasks_Goal goal;
} yaskawa_msgs__action__YaskawaTasks_SendGoal_Request;

// Struct for a sequence of yaskawa_msgs__action__YaskawaTasks_SendGoal_Request.
typedef struct yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence
{
  yaskawa_msgs__action__YaskawaTasks_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/YaskawaTasks in the package yaskawa_msgs.
typedef struct yaskawa_msgs__action__YaskawaTasks_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} yaskawa_msgs__action__YaskawaTasks_SendGoal_Response;

// Struct for a sequence of yaskawa_msgs__action__YaskawaTasks_SendGoal_Response.
typedef struct yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence
{
  yaskawa_msgs__action__YaskawaTasks_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/YaskawaTasks in the package yaskawa_msgs.
typedef struct yaskawa_msgs__action__YaskawaTasks_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} yaskawa_msgs__action__YaskawaTasks_GetResult_Request;

// Struct for a sequence of yaskawa_msgs__action__YaskawaTasks_GetResult_Request.
typedef struct yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence
{
  yaskawa_msgs__action__YaskawaTasks_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "yaskawa_msgs/action/detail/yaskawa_tasks__struct.h"

/// Struct defined in action/YaskawaTasks in the package yaskawa_msgs.
typedef struct yaskawa_msgs__action__YaskawaTasks_GetResult_Response
{
  int8_t status;
  yaskawa_msgs__action__YaskawaTasks_Result result;
} yaskawa_msgs__action__YaskawaTasks_GetResult_Response;

// Struct for a sequence of yaskawa_msgs__action__YaskawaTasks_GetResult_Response.
typedef struct yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence
{
  yaskawa_msgs__action__YaskawaTasks_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "yaskawa_msgs/action/detail/yaskawa_tasks__struct.h"

/// Struct defined in action/YaskawaTasks in the package yaskawa_msgs.
typedef struct yaskawa_msgs__action__YaskawaTasks_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  yaskawa_msgs__action__YaskawaTasks_Feedback feedback;
} yaskawa_msgs__action__YaskawaTasks_FeedbackMessage;

// Struct for a sequence of yaskawa_msgs__action__YaskawaTasks_FeedbackMessage.
typedef struct yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence
{
  yaskawa_msgs__action__YaskawaTasks_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__STRUCT_H_
