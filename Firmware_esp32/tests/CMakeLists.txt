cmake_minimum_required(VERSION 3.16)
project(PickUSPlacUSHostTests LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.15.2.zip
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(host_tests
    host/tests/command_handler_test.cpp
    host/tests/controller_test.cpp
    host/tests/communication_handler_test.cpp
    host/tests/data_handler_test.cpp
    host/tests/home_command_test.cpp
    host/tests/move_command_test.cpp
    host/tests/pick_command_test.cpp
    host/tests/place_command_test.cpp
    host/tests/pause_command_test.cpp
    host/tests/stop_command_test.cpp
    host/tests/pump_command_test.cpp
    host/tests/valve_command_test.cpp
    host/stubs/Arduino.cpp
    ../src/CommunicationHandler.cpp
    ../src/CommandHandler.cpp
    ../src/Controller.cpp
    ../src/DataHandler.cpp
    ../src/commands/HomeCommand.cpp
    ../src/commands/MoveCommand.cpp
    ../src/commands/PickCommand.cpp
    ../src/commands/PlaceCommand.cpp
    ../src/commands/PauseCommand.cpp
    ../src/commands/StopCommand.cpp
    ../src/commands/PumpCommand.cpp
    ../src/commands/ValveCommand.cpp
)

target_include_directories(host_tests PRIVATE
    host/stubs
    ../src
    ../lib
)

target_link_libraries(host_tests PRIVATE GTest::gtest_main)

target_compile_definitions(host_tests PRIVATE HOST_TEST=1)

include(GoogleTest)
gtest_discover_tests(host_tests)
