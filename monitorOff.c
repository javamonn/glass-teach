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

//1 - screen is enabled and usable. 0 - Screen is disabled, user input is blocked
char screenEnabled;

//constants
char FILE_PATH[] = "T:\Get Assignments\Tech_Apps\Cadle, Aaron\UIL\glass-test.txt";

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
  
  //create thread to read shared file and post messages to this thread
  windowManagerHandle = CreateThread(NULL, 0, WindowManager, 0, 0, NULL);
  
  
  HWND window = disable(&wc, &mi);
  Sleep(500);
  enable(window);
}

void WindowManager() {

  LPSYSTEMTIME systemTime;
  FILETIME systemTimeAsFileTime;
  FILETIME fileTime;
  HANDLE file;

  //done at startup, at this point there should be nothing in the file
  file = CreateFile(FILE_PATH,
                    GENERIC_READ,
   			        FILE_SHARE_READ,
				    NULL,
				    OPEN_EXISTING,
				    FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED,
				    NULL);
  if (file == INVALID_HANDLE_VALUE) {
	tprintf(TEXT("Unable to open file"));
	exit(-1);
  }
  
  screenEnabled = '1';
  
  /* Every so often read the file we're watching, if anything is different from the current state of the computer
   * we take actions to match it. Structure of file is just a 1 line string of 1's and 0's. First is used to denote
   * screen enabled or disabled. Some of these values will be toggled, ie read and then flipped. These are used for
   * data requesting. Format of this will probably change as time goes by.
   */
  while(true) {
    //big enough for now lol
    char fileData[10] = {};
	DWORD bytesRead = -1;
	ReadFile(file, (LPVOID) &fileData, 10, &bytesRead, NULL);
	
	//enable/disable screen char
	if (fileData[0] != screenEnabled) {
	  if (fileData[0] == '1') {
	    //enable screen
	    
	  }
	  else {
	    //disable screen
	  }
	  screenEnabled = fileData[0];
	}
	
	//check file again a second later
	Sleep(1000);
  }
}

HWND disable(WNDCLASSW *wc, MONITORINFO *mi) {
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
  printf("end message loop\n");
  return window;
}

int enable(HWND window) {
  printf("enable window\n");
  (blockInput) (FALSE);
  printf("%d\n", DestroyWindow(window));
  printf("%d\n", GetLastError());
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

void CenterWindow(HWND hwnd)
{
  RECT rc;
  GetWindowRect(hwnd, &rc) ; 
  SetWindowPos(hwnd, 0, 
              (GetSystemMetrics(SM_CXSCREEN) - rc.right)/2,
              (GetSystemMetrics(SM_CYSCREEN) - rc.bottom)/2,
              0, 0, SWP_NOZORDER|SWP_NOSIZE);
}
