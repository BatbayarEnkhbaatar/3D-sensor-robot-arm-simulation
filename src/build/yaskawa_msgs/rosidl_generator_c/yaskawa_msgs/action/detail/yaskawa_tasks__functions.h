// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from yaskawa_msgs:action/YaskawaTasks.idl
// generated code does not contain a copyright notice

#ifndef YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__FUNCTIONS_H_
#define YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "yaskawa_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "yaskawa_msgs/action/detail/yaskawa_tasks__struct.h"

/// Initialize action/YaskawaTasks message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * yaskawa_msgs__action__YaskawaTasks_Goal
 * )) before or use
 * yaskawa_msgs__action__YaskawaTasks_Goal__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Goal__init(yaskawa_msgs__action__YaskawaTasks_Goal * msg);

/// Finalize action/YaskawaTasks message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Goal__fini(yaskawa_msgs__action__YaskawaTasks_Goal * msg);

/// Create action/YaskawaTasks message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * yaskawa_msgs__action__YaskawaTasks_Goal__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_Goal *
yaskawa_msgs__action__YaskawaTasks_Goal__create();

/// Destroy action/YaskawaTasks message.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_Goal__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Goal__destroy(yaskawa_msgs__action__YaskawaTasks_Goal * msg);

/// Check for action/YaskawaTasks message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Goal__are_equal(const yaskawa_msgs__action__YaskawaTasks_Goal * lhs, const yaskawa_msgs__action__YaskawaTasks_Goal * rhs);

/// Copy a action/YaskawaTasks message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Goal__copy(
  const yaskawa_msgs__action__YaskawaTasks_Goal * input,
  yaskawa_msgs__action__YaskawaTasks_Goal * output);

/// Initialize array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the number of elements and calls
 * yaskawa_msgs__action__YaskawaTasks_Goal__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Goal__Sequence__init(yaskawa_msgs__action__YaskawaTasks_Goal__Sequence * array, size_t size);

/// Finalize array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_Goal__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Goal__Sequence__fini(yaskawa_msgs__action__YaskawaTasks_Goal__Sequence * array);

/// Create array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the array and calls
 * yaskawa_msgs__action__YaskawaTasks_Goal__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_Goal__Sequence *
yaskawa_msgs__action__YaskawaTasks_Goal__Sequence__create(size_t size);

/// Destroy array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_Goal__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Goal__Sequence__destroy(yaskawa_msgs__action__YaskawaTasks_Goal__Sequence * array);

/// Check for action/YaskawaTasks message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Goal__Sequence__are_equal(const yaskawa_msgs__action__YaskawaTasks_Goal__Sequence * lhs, const yaskawa_msgs__action__YaskawaTasks_Goal__Sequence * rhs);

/// Copy an array of action/YaskawaTasks messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Goal__Sequence__copy(
  const yaskawa_msgs__action__YaskawaTasks_Goal__Sequence * input,
  yaskawa_msgs__action__YaskawaTasks_Goal__Sequence * output);

/// Initialize action/YaskawaTasks message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * yaskawa_msgs__action__YaskawaTasks_Result
 * )) before or use
 * yaskawa_msgs__action__YaskawaTasks_Result__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Result__init(yaskawa_msgs__action__YaskawaTasks_Result * msg);

/// Finalize action/YaskawaTasks message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Result__fini(yaskawa_msgs__action__YaskawaTasks_Result * msg);

/// Create action/YaskawaTasks message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * yaskawa_msgs__action__YaskawaTasks_Result__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_Result *
yaskawa_msgs__action__YaskawaTasks_Result__create();

/// Destroy action/YaskawaTasks message.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_Result__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Result__destroy(yaskawa_msgs__action__YaskawaTasks_Result * msg);

/// Check for action/YaskawaTasks message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Result__are_equal(const yaskawa_msgs__action__YaskawaTasks_Result * lhs, const yaskawa_msgs__action__YaskawaTasks_Result * rhs);

/// Copy a action/YaskawaTasks message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Result__copy(
  const yaskawa_msgs__action__YaskawaTasks_Result * input,
  yaskawa_msgs__action__YaskawaTasks_Result * output);

/// Initialize array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the number of elements and calls
 * yaskawa_msgs__action__YaskawaTasks_Result__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Result__Sequence__init(yaskawa_msgs__action__YaskawaTasks_Result__Sequence * array, size_t size);

/// Finalize array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_Result__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Result__Sequence__fini(yaskawa_msgs__action__YaskawaTasks_Result__Sequence * array);

/// Create array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the array and calls
 * yaskawa_msgs__action__YaskawaTasks_Result__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_Result__Sequence *
yaskawa_msgs__action__YaskawaTasks_Result__Sequence__create(size_t size);

/// Destroy array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_Result__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Result__Sequence__destroy(yaskawa_msgs__action__YaskawaTasks_Result__Sequence * array);

/// Check for action/YaskawaTasks message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Result__Sequence__are_equal(const yaskawa_msgs__action__YaskawaTasks_Result__Sequence * lhs, const yaskawa_msgs__action__YaskawaTasks_Result__Sequence * rhs);

/// Copy an array of action/YaskawaTasks messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Result__Sequence__copy(
  const yaskawa_msgs__action__YaskawaTasks_Result__Sequence * input,
  yaskawa_msgs__action__YaskawaTasks_Result__Sequence * output);

/// Initialize action/YaskawaTasks message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * yaskawa_msgs__action__YaskawaTasks_Feedback
 * )) before or use
 * yaskawa_msgs__action__YaskawaTasks_Feedback__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Feedback__init(yaskawa_msgs__action__YaskawaTasks_Feedback * msg);

/// Finalize action/YaskawaTasks message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Feedback__fini(yaskawa_msgs__action__YaskawaTasks_Feedback * msg);

/// Create action/YaskawaTasks message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * yaskawa_msgs__action__YaskawaTasks_Feedback__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_Feedback *
yaskawa_msgs__action__YaskawaTasks_Feedback__create();

/// Destroy action/YaskawaTasks message.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_Feedback__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Feedback__destroy(yaskawa_msgs__action__YaskawaTasks_Feedback * msg);

/// Check for action/YaskawaTasks message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Feedback__are_equal(const yaskawa_msgs__action__YaskawaTasks_Feedback * lhs, const yaskawa_msgs__action__YaskawaTasks_Feedback * rhs);

/// Copy a action/YaskawaTasks message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Feedback__copy(
  const yaskawa_msgs__action__YaskawaTasks_Feedback * input,
  yaskawa_msgs__action__YaskawaTasks_Feedback * output);

/// Initialize array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the number of elements and calls
 * yaskawa_msgs__action__YaskawaTasks_Feedback__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence__init(yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence * array, size_t size);

/// Finalize array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_Feedback__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence__fini(yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence * array);

/// Create array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the array and calls
 * yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence *
yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence__create(size_t size);

/// Destroy array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence__destroy(yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence * array);

/// Check for action/YaskawaTasks message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence__are_equal(const yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence * lhs, const yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence * rhs);

/// Copy an array of action/YaskawaTasks messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence__copy(
  const yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence * input,
  yaskawa_msgs__action__YaskawaTasks_Feedback__Sequence * output);

/// Initialize action/YaskawaTasks message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Request
 * )) before or use
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__init(yaskawa_msgs__action__YaskawaTasks_SendGoal_Request * msg);

/// Finalize action/YaskawaTasks message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__fini(yaskawa_msgs__action__YaskawaTasks_SendGoal_Request * msg);

/// Create action/YaskawaTasks message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request *
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__create();

/// Destroy action/YaskawaTasks message.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__destroy(yaskawa_msgs__action__YaskawaTasks_SendGoal_Request * msg);

/// Check for action/YaskawaTasks message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__are_equal(const yaskawa_msgs__action__YaskawaTasks_SendGoal_Request * lhs, const yaskawa_msgs__action__YaskawaTasks_SendGoal_Request * rhs);

/// Copy a action/YaskawaTasks message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__copy(
  const yaskawa_msgs__action__YaskawaTasks_SendGoal_Request * input,
  yaskawa_msgs__action__YaskawaTasks_SendGoal_Request * output);

/// Initialize array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the number of elements and calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence__init(yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence * array, size_t size);

/// Finalize array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence__fini(yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence * array);

/// Create array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the array and calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence *
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence__create(size_t size);

/// Destroy array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence__destroy(yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence * array);

/// Check for action/YaskawaTasks message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence__are_equal(const yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence * lhs, const yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence * rhs);

/// Copy an array of action/YaskawaTasks messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence__copy(
  const yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence * input,
  yaskawa_msgs__action__YaskawaTasks_SendGoal_Request__Sequence * output);

/// Initialize action/YaskawaTasks message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Response
 * )) before or use
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__init(yaskawa_msgs__action__YaskawaTasks_SendGoal_Response * msg);

/// Finalize action/YaskawaTasks message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__fini(yaskawa_msgs__action__YaskawaTasks_SendGoal_Response * msg);

/// Create action/YaskawaTasks message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response *
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__create();

/// Destroy action/YaskawaTasks message.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__destroy(yaskawa_msgs__action__YaskawaTasks_SendGoal_Response * msg);

/// Check for action/YaskawaTasks message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__are_equal(const yaskawa_msgs__action__YaskawaTasks_SendGoal_Response * lhs, const yaskawa_msgs__action__YaskawaTasks_SendGoal_Response * rhs);

/// Copy a action/YaskawaTasks message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__copy(
  const yaskawa_msgs__action__YaskawaTasks_SendGoal_Response * input,
  yaskawa_msgs__action__YaskawaTasks_SendGoal_Response * output);

/// Initialize array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the number of elements and calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence__init(yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence * array, size_t size);

/// Finalize array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence__fini(yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence * array);

/// Create array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the array and calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence *
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence__create(size_t size);

/// Destroy array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence__destroy(yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence * array);

/// Check for action/YaskawaTasks message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence__are_equal(const yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence * lhs, const yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence * rhs);

/// Copy an array of action/YaskawaTasks messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence__copy(
  const yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence * input,
  yaskawa_msgs__action__YaskawaTasks_SendGoal_Response__Sequence * output);

/// Initialize action/YaskawaTasks message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Request
 * )) before or use
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__init(yaskawa_msgs__action__YaskawaTasks_GetResult_Request * msg);

/// Finalize action/YaskawaTasks message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__fini(yaskawa_msgs__action__YaskawaTasks_GetResult_Request * msg);

/// Create action/YaskawaTasks message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_GetResult_Request *
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__create();

/// Destroy action/YaskawaTasks message.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__destroy(yaskawa_msgs__action__YaskawaTasks_GetResult_Request * msg);

/// Check for action/YaskawaTasks message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__are_equal(const yaskawa_msgs__action__YaskawaTasks_GetResult_Request * lhs, const yaskawa_msgs__action__YaskawaTasks_GetResult_Request * rhs);

/// Copy a action/YaskawaTasks message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__copy(
  const yaskawa_msgs__action__YaskawaTasks_GetResult_Request * input,
  yaskawa_msgs__action__YaskawaTasks_GetResult_Request * output);

/// Initialize array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the number of elements and calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence__init(yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence * array, size_t size);

/// Finalize array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence__fini(yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence * array);

/// Create array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the array and calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence *
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence__create(size_t size);

/// Destroy array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence__destroy(yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence * array);

/// Check for action/YaskawaTasks message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence__are_equal(const yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence * lhs, const yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence * rhs);

/// Copy an array of action/YaskawaTasks messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence__copy(
  const yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence * input,
  yaskawa_msgs__action__YaskawaTasks_GetResult_Request__Sequence * output);

/// Initialize action/YaskawaTasks message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Response
 * )) before or use
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__init(yaskawa_msgs__action__YaskawaTasks_GetResult_Response * msg);

/// Finalize action/YaskawaTasks message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__fini(yaskawa_msgs__action__YaskawaTasks_GetResult_Response * msg);

/// Create action/YaskawaTasks message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_GetResult_Response *
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__create();

/// Destroy action/YaskawaTasks message.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__destroy(yaskawa_msgs__action__YaskawaTasks_GetResult_Response * msg);

/// Check for action/YaskawaTasks message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__are_equal(const yaskawa_msgs__action__YaskawaTasks_GetResult_Response * lhs, const yaskawa_msgs__action__YaskawaTasks_GetResult_Response * rhs);

/// Copy a action/YaskawaTasks message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__copy(
  const yaskawa_msgs__action__YaskawaTasks_GetResult_Response * input,
  yaskawa_msgs__action__YaskawaTasks_GetResult_Response * output);

/// Initialize array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the number of elements and calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence__init(yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence * array, size_t size);

/// Finalize array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence__fini(yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence * array);

/// Create array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the array and calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence *
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence__create(size_t size);

/// Destroy array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence__destroy(yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence * array);

/// Check for action/YaskawaTasks message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence__are_equal(const yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence * lhs, const yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence * rhs);

/// Copy an array of action/YaskawaTasks messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence__copy(
  const yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence * input,
  yaskawa_msgs__action__YaskawaTasks_GetResult_Response__Sequence * output);

/// Initialize action/YaskawaTasks message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * yaskawa_msgs__action__YaskawaTasks_FeedbackMessage
 * )) before or use
 * yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__init(yaskawa_msgs__action__YaskawaTasks_FeedbackMessage * msg);

/// Finalize action/YaskawaTasks message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__fini(yaskawa_msgs__action__YaskawaTasks_FeedbackMessage * msg);

/// Create action/YaskawaTasks message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage *
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__create();

/// Destroy action/YaskawaTasks message.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__destroy(yaskawa_msgs__action__YaskawaTasks_FeedbackMessage * msg);

/// Check for action/YaskawaTasks message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__are_equal(const yaskawa_msgs__action__YaskawaTasks_FeedbackMessage * lhs, const yaskawa_msgs__action__YaskawaTasks_FeedbackMessage * rhs);

/// Copy a action/YaskawaTasks message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__copy(
  const yaskawa_msgs__action__YaskawaTasks_FeedbackMessage * input,
  yaskawa_msgs__action__YaskawaTasks_FeedbackMessage * output);

/// Initialize array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the number of elements and calls
 * yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence__init(yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence * array, size_t size);

/// Finalize array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence__fini(yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence * array);

/// Create array of action/YaskawaTasks messages.
/**
 * It allocates the memory for the array and calls
 * yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence *
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence__create(size_t size);

/// Destroy array of action/YaskawaTasks messages.
/**
 * It calls
 * yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
void
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence__destroy(yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence * array);

/// Check for action/YaskawaTasks message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence__are_equal(const yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence * lhs, const yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence * rhs);

/// Copy an array of action/YaskawaTasks messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_yaskawa_msgs
bool
yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence__copy(
  const yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence * input,
  yaskawa_msgs__action__YaskawaTasks_FeedbackMessage__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // YASKAWA_MSGS__ACTION__DETAIL__YASKAWA_TASKS__FUNCTIONS_H_
