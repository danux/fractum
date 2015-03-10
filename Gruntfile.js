module.exports = function(grunt) {
  require('jit-grunt')(grunt);

  grunt.initConfig({
    uglify: {
      options: {
          compress: false,
          mangle: false
      },
      my_target: {
        files: {
          'static/js/main.min.js': ['resources/js/*.js']
        }
      }
    },
    less: {
      development: {
        options: {
          compress: true,
          yuicompress: true,
          optimization: 2
        },
        files: {
          "static/css/main.css": "resources/less/main.less"
        }
      }
    },
    watch: {
      styles: {
        files: ['resources/js/*.js', 'resources/less/**/*.less'],
        tasks: ['uglify', 'less'],
        options: {
          nospawn: true
        }
      }
    },
    copy: {
      fonts: {
        expand: true,
        cwd: 'resources/fonts/',
        src: '**',
        dest: 'static/fonts/',
        flatten: true,
        filter: 'isFile'
      },
      images: {
        expand: true,
        cwd: 'resources/images/',
        src: '**',
        dest: 'static/images/',
        flatten: true,
        filter: 'isFile'
      }
    }
  });
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('build', ['less', 'uglify', 'copy:fonts', 'copy:images']);
  grunt.registerTask('dev', ['build', 'watch']);
  grunt.registerTask('default', ['dev']);
};
