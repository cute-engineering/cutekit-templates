#include <raylib.h>

int main(int argc, char **argv) {
  (void)argc;
  (void)argv;
  const int screenWidth = 800;
  const int screenHeight = 450;

  InitWindow(screenWidth, screenHeight, "raylib [core] example - basic window");

  SetTargetFPS(60);
  while (!WindowShouldClose()) {
    BeginDrawing();

    ClearBackground(RAYWHITE);

    DrawText("Congrats! \nYou created your first raylib window\nAnd built the "
             "project using cutekit !",
             150, 200, 20, BLACK);

    EndDrawing();
  }

  CloseWindow();
  return 0;
}