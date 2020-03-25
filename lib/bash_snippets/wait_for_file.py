def wait_for_file(file, max_seconds):
  iterations = max_seconds * 10
  return (
    "for i in $(seq 0 %s)\n"
    "do\n"
    "  if [ -f %s ]; then\n"
    "    break\n"
    "  fi\n"
    "  sleep 0.1\n"
    "done"
  ) % (iterations, file)


# if __name__ == '__main__':
#   assert wait_for_file('a file') == "while [ ! -f a file ]\ndo\n  sleep 0.1\ndone", wait_for_file('a file')