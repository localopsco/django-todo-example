{{- define "postgresql.host" -}}
{{- printf "%s-postgresql" .Release.Name -}}
{{- end -}}
