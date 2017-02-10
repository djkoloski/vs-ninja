import os
import fnmatch
import ninja_syntax

# Get general paths
project_path = os.path.dirname(os.path.realpath(__file__))
solution_path = os.path.dirname(project_path)
project_name = os.path.basename(project_path)
solution_name = os.path.basename(solution_path)

# Get build and bin paths for x86/x64 and Debug/Release
build_x64_path = os.path.join(project_path, 'x64')
build_release_x86_path = os.path.join(project_path, 'Release')
build_debug_x86_path = os.path.join(project_path, 'Debug')
build_release_x64_path = os.path.join(build_x64_path, 'Release')
build_debug_x64_path = os.path.join(build_x64_path, 'Debug')

bin_x64_path = os.path.join(solution_path, 'x64')
bin_release_x86_path = os.path.join(solution_path, 'Release')
bin_debug_x86_path = os.path.join(solution_path, 'Debug')
bin_release_x64_path = os.path.join(bin_x64_path, 'Release')
bin_debug_x64_path = os.path.join(bin_x64_path, 'Debug')

# Open build file for write
build_filename = os.path.join(project_path, 'build.ninja')
n = ninja_syntax.Writer(open(build_filename, 'w'))

# Set up variables
objext = '.obj'
binext = '.exe'

n.variable('cxx', 'cl')
n.variable('py', 'py')

# Common flags
n.variable('cflags', ' '.join([
	'/I', solution_path,
	'/EHsc',
	'/showIncludes']))

# Release-only flags
n.variable('crelflags', ' '.join([
	]))
# Debug-only flags
n.variable('cdbgflags', ' '.join([
	'/DEBUG']))
# x86-only flags
n.variable('cx86flags', ' '.join([
	]))
# x64-only flags
n.variable('cx64flags', ' '.join([
	]))

# Add CXX rules
n.rule('cxx-release-x86',
	command='$cxx $cflags -c $in $crelflags $cx86flags /Fo$out',
	deps='msvc',
	description='CXX $out')
n.rule('cxx-debug-x86',
	command='$cxx $cflags -c $in $cdbgflags $cx86flags /Fo$out',
	deps='msvc',
	description='CXX $out')
n.rule('cxx-release-x64',
	command='$cxx $cflags -c $in $crelflags $cx64flags /Fo$out',
	deps='msvc',
	description='CXX $out')
n.rule('cxx-debug-x64',
	command='$cxx $cflags -c $in $cdbgflags $cx64flags /Fo$out',
	deps='msvc',
	description='CXX $out')

# Add link rules
n.rule('link-release-x86',
	command='$cxx $in $libs /nologo /link $ldflags $crelflags $cx86flags /out:$out',
	description='LINK $out')
n.rule('link-debug-x86',
	command='$cxx $in $libs /nologo /link $ldflags $cdbgflags $cx86flags /out:$out',
	description='LINK $out')
n.rule('link-release-x64',
	command='$cxx $in $libs /nologo /link $ldflags $crelflags $cx64flags /out:$out',
	description='LINK $out')
n.rule('link-debug-x64',
	command='$cxx $in $libs /nologo /link $ldflags $cdbgflags $cx64flags /out:$out',
	description='LINK $out')

# Add configure rule
n.rule('configure',
	command='$py $in',
	description='py $in',
	generator=True)


# Add CPP builds
cpp_paths = [os.path.join(dirpath, f)
	for dirpath, dirnames, files in os.walk(project_path)
	for f in fnmatch.filter(files, '*.cpp')]
cpp_sources = [os.path.relpath(path, project_path) for path in cpp_paths]
cpp_objects = [os.path.splitext(path)[0] + objext for path in cpp_sources]
for i in range(len(cpp_sources)):
	n.build(
		os.path.join(build_release_x86_path, cpp_objects[i]),
		'cxx-release-x86',
		os.path.join(project_path, cpp_sources[i]))
	n.build(
		os.path.join(build_debug_x86_path, cpp_objects[i]),
		'cxx-debug-x86',
		os.path.join(project_path, cpp_sources[i]))
	n.build(
		os.path.join(build_release_x64_path, cpp_objects[i]),
		'cxx-release-x64',
		os.path.join(project_path, cpp_sources[i]))
	n.build(
		os.path.join(build_debug_x64_path, cpp_objects[i]),
		'cxx-debug-x64',
		os.path.join(project_path, cpp_sources[i]))

# Add executable builds
n.build(
	os.path.join(bin_release_x86_path, project_name + binext),
	'link-release-x86',
	[os.path.join(build_release_x86_path, path) for path in cpp_objects])
n.build(
	os.path.join(bin_debug_x86_path, project_name + binext),
	'link-debug-x86',
	[os.path.join(build_debug_x86_path, path) for path in cpp_objects])
n.build(
	os.path.join(bin_release_x64_path, project_name + binext),
	'link-release-x64',
	[os.path.join(build_release_x64_path, path) for path in cpp_objects])
n.build(
	os.path.join(bin_debug_x64_path, project_name + binext),
	'link-debug-x64',
	[os.path.join(build_debug_x64_path, path) for path in cpp_objects])

# Add configuring
n.build(
	os.path.join(project_path, 'build.ninja'),
	'configure',
	os.path.join(project_path, 'configure.py'))