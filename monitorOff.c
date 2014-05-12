#include <windows.h>
#include <stdio.h>

//gcc monitorOff.c -lgdi32

/**
 * THIS IS THE CLIENT TO BE RUN ON STUDENT COMPUTERS
 * This will monitor the file that the google glass will push commands to, enabling and disabling monitors
 */

//internally defined functions
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
HWND disable(WNDCLASSW *, MONITORINFO *);
int enable(HWND);
void CenterWindow(HWND);

//functions pulled from .dll
typedef int (__cdecl *BlockInput)(BOOL);

//globals
BlockInput blockInput;
HINSTANCE hInstGlobal;
HINSTANCE hInstUser;

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                    LPSTR lpCmdLine, int nCmdShow)
{
  //
  HMONITOR hmon;
  MONITORINFO mi;
  HANDLE windowManagerHandle;
  
  //wndclass instantiation
  WNDCLASSW wc = {0};
  wc.lpszClassName = L"Glass-Teach";
  wc.hInstance     = hInstance;
  wc.hbrBackground = CreateSolidBrush(RGB(0, 0, 0));
  wc.lpfnWndProc   = WndProc;
  wc.hCursor       = LoadCursor(0, IDC_ARROW);
  RegisterClassW(&wc);

  //info needed for fullscreen window
  hInstGlobal = hInstance;
  hmon = MonitorFromWindow(GetDesktopWindow(), MONITOR_DEFAULTTONEAREST);
  mi = { sizeof(mi) };
  if (!GetMonitorInfo(hmon, &mi)) return -1;
  
  //load the block input function
  hInstUser = LoadLibrary(TEXT("user32.dll"));
  blockInput = (BlockInput) GetProcAddress(hInstUser, "BlockInput");
  MSG msg;
  HWND window;
  //block all input (CTRL ALT DEL will still exit from this)
  (blockInput) (TRUE);
  //create full screen black window, hide cursor
  window = CreateWindowW(wc->lpszClassName, L"Center",
				WS_POPUP | WS_VISIBLE,
				mi->rcMonitor.left,
				mi->rcMonitor.top,
				mi->rcMonitor.right - mi->rcMonitor.left,
				mi->rcMonitor.bottom - mi->rcMonitor.top,
				0, 0, hInstGlobal, 0);
  printf("begin message loop\n");
  /* Message loop, window waits until recieving a command to renable window
   *
   */
  while(GetMessage(&msg, window, 0, 0)) {
    TranslateMessage(&msg);
    DispatchMessage(&msg);
  }
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, 
    WPARAM wParam, LPARAM lParam)
{
  switch(msg)  
  {
	  //can this create a window on demand? WndProc is registered with WNDCLASSW, independent of the window 
      case WM_CREATE:
      {
          CenterWindow(hwnd);
          return 0;
      }

      case WM_DESTROY:
      {
          PostQuitMessage(0);
	      FreeLibrary(hInstUser);
          return 0;
      }
      case WM_SETCURSOR:
      {
          SetCursor(NULL);
	      return 0;
      }
  }

  return DefWindowProcW(hwnd, msg, wParam, lParam);
}
